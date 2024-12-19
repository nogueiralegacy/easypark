# Estágio de build
FROM node:18-alpine as construtor

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependência
COPY package*.json ./

# Instalar dependências
RUN npm ci

# Copiar todo o código fonte
COPY . .

# Construir o projeto
RUN npm run build

# Estágio final
FROM node:18-alpine

# Instalar serve globalmente
RUN npm install -g serve

# Copiar build do estágio anterior
COPY --from=construtor /app/build /app/build

# Definir diretório de trabalho
WORKDIR /app

# Expor porta 80
EXPOSE 80

# Comando para iniciar o servidor
ENTRYPOINT ["serve", "-s", "build", "-l", "80"]