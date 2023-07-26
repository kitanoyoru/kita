package cfg

import (
	"fmt"
	"net/url"

	"github.com/spf13/viper"
)

type ServerConfig struct {
	Port string `mapstructure:"port"`
}

type DatabaseConfig struct {
	Host     string `mapstructure:"host"`
	Port     string `mapstructure:"port"`
	Name     string `mapstructure:"name"`
	User     string `mapstructure:"user"`
	Password string `mapstructure:"password"`
}

func (dc *DatabaseConfig) ToUrl() string {
	u := &url.URL{
		Scheme: "http",
		Host:   fmt.Sprintf("%s:%s", dc.Host, dc.Port),
	}

	return u.String()
}

type Config struct {
	Debug bool `mapstructure:"bool"`

	Server   *ServerConfig   `mapstructure:"server"`
	Database *DatabaseConfig `mapstructure:"database"`
}

func NewConfig() (*Config, error) {
	v := viper.New()
	v.SetConfigFile(DefaultConfigPath)

	var config Config
	if err := v.ReadInConfig(); err != nil {
		return nil, err
	}

	if err := v.Unmarshal(&config); err != nil {
		return nil, err
	}

	return &config, nil
}