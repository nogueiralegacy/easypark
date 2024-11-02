#!/bin/bash

# Verifica se o plantuml.jar existe na pasta
if [ ! -f "./input-cache/plantuml.jar" ]; then
    echo "plantuml.jar não encontrado na pasta input-cache/"
    
    echo "Criando diretório input-cache se não existir..."
    mkdir -p ./input-cache
    
    echo "Download plantuml.jar..."
    wget -q -O ./input-cache/plantuml.jar "https://github.com/plantuml/plantuml/releases/download/v1.2024.7/plantuml-1.2024.7.jar"
    
    if [ $? -eq 0 ]; then
        echo "Download concluído com sucesso"
    else
        echo "Falha no download. Por favor, verifique sua conexão e tente novamente."
        exit 1
    fi
else
    echo "plantuml.jar localizado na pasta input-cache"
fi

java -jar ./input-cache/plantuml.jar *.puml

echo "Imagens geradas com sucesso"