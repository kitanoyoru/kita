package app

import (
	"context"
	"log"
	"strings"
	"time"

	grpcc "github.com/go-micro/plugins/v4/client/grpc"
	"github.com/go-micro/plugins/v4/registry/kubernetes"
	grpcs "github.com/go-micro/plugins/v4/server/grpc"
	"github.com/go-micro/plugins/v4/wrapper/trace/opentelemetry"
	"go-micro.dev/v4"
	"go-micro.dev/v4/server"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/propagation"

	_ "github.com/go-micro/plugins/v4/registry/kubernetes"
	"github.com/kitanoyoru/kita/apps/email/internal/config"
	"github.com/kitanoyoru/kita/apps/email/internal/handlers"
	"github.com/kitanoyoru/kita/apps/email/internal/middlewares"
	"github.com/kitanoyoru/kita/apps/email/internal/providers"

	pb "github.com/kitanoyoru/kita/apps/email/pkg/proto"
)

// TODO: helath checker
// TODO: service status (ram, cpu, hdd etc)

type App struct {
	name    string
	version string

	srv micro.Service
}

func NewApp(name, version string) *App {
	srv := micro.NewService(
		micro.Server(grpcs.NewServer()),
		micro.Client(grpcc.NewClient()),
	)

	return &App{
		name,
		version,
		srv,
	}
}

func (app *App) Init() error {
	registry := kubernetes.NewRegistry()

	opts := []micro.Option{
		micro.Name(app.name),
		micro.Version(app.version),
		micro.Address(config.Address()),
		micro.Registry(registry),
		micro.WrapHandler(middlewares.LogMiddleware),
	}

	if cfg := config.Tracing(); cfg.Enable {
		tp, err := providers.NewTracerProvider(app.srv.Server().Options().Id, app.name, app.version, cfg.Jaeger.URL)
		if err != nil {
			return err
		}

		defer func() {
			ctx, cancel := context.WithTimeout(context.Background(), time.Second*5)
			defer cancel()

			if err := tp.Shutdown(ctx); err != nil {
				log.Fatal(err)
			}
		}()

		otel.SetTracerProvider(tp)
		otel.SetTextMapPropagator(propagation.NewCompositeTextMapPropagator(propagation.TraceContext{}, propagation.Baggage{}))

		traceOpts := []opentelemetry.Option{
			opentelemetry.WithHandleFilter(func(ctx context.Context, r server.Request) bool {
				if e := r.Endpoint(); strings.HasPrefix(e, "Health.") {
					return true
				}
				return false
			}),
		}

		opts = append(opts, micro.WrapHandler(opentelemetry.NewHandlerWrapper(traceOpts...)))
	}

	app.srv.Init(opts...)

	if err := app.registerHandlers(); err != nil {
		return err
	}

	return nil
}

func (app *App) Run() error {
	return app.srv.Run()
}

func (app *App) registerHandlers() error {
	if err := pb.RegisterEmailServiceHandler(app.srv.Server(), handlers.NewEmail()); err != nil {
		return err
	}

	if err := pb.RegisterHealthHandler(app.srv.Server(), new(handlers.Health)); err != nil {
		return err
	}

	return nil
}
