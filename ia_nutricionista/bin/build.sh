#!/bin/bash

# Definição de cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
NC='\033[0m' # Sem cor

echo -e "${BLUE}========================================="
echo -e "      🚀 Iniciando o Projeto"
echo -e "=========================================${NC}\n"

# Verifica se a network 'asimov' existe
echo -e "${YELLOW}🔍 Verificando se a network Docker 'asimov' existe...${NC}"
if ! docker network inspect asimov >/dev/null 2>&1; then
    echo -e "${YELLOW}➡️  A network 'asimov' não existe. Criando...${NC}"
    if docker network create asimov; then
        echo -e "${GREEN}✅ Network 'asimov' criada com sucesso!${NC}\n"
    else
        echo -e "${RED}❌ Erro ao criar a network 'asimov'. Abortando.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ A network 'asimov' já existe.${NC}\n"
fi

# Exporta o requirements.txt a partir do Poetry
echo -e "${YELLOW}📦 Exportando dependências do Poetry para o arquivo requirements.txt...${NC}"
if poetry export -f requirements.txt --output requirements.txt --without-hashes; then
    echo -e "${GREEN}✅ requirements.txt exportado com sucesso!${NC}\n"
else
    echo -e "${RED}❌ Erro ao exportar o arquivo requirements.txt.${NC}"
    exit 1
fi

# Sobe o projeto com Docker Compose
echo -e "${YELLOW}🛠  Subindo o projeto com Docker Compose...${NC}"
if docker compose up -d --build --remove-orphans --force-recreate; then
    echo -e "${GREEN}✅ Projeto iniciado com sucesso!${NC}"
else
    echo -e "${RED}❌ Erro ao iniciar o projeto com Docker Compose.${NC}"
    exit 1
fi

echo -e "\n${BLUE}========================================="
echo -e "      🎉 Aplicação em Funcionamento"
echo -e "=========================================${NC}"
