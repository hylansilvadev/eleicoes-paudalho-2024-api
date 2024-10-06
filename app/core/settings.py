from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Configurações do modelo Pydantic
    model_config = SettingsConfigDict(
        env_file='.env',  # Arquivo .env contendo as variáveis de ambiente
        env_file_encoding='utf-8',  # Codificação do arquivo
        env_ignore_empty=True  # Ignorar variáveis vazias no arquivo .env
    )
    
    # Definição das variáveis de ambiente esperadas
    MONGODB_URL: str
    DATABASE_NAME: str
    URL_PREFEITO: str
    URL_VEREADORES: str

# Instanciando as configurações
settings = Settings()
