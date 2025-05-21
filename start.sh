#!/bin/bash

# Par défaut dev si ENV non défini
ENV=${ENV:-dev}

echo "Activation de l'environnement virtuel Poetry..."
source /Users/mac7/Library/Caches/pypoetry/virtualenvs/invoice-backend-8xC5eWan-py3.11/bin/activate


echo "Lancement de l'application avec ENV=$ENV"

export ENV=$ENV

uvicorn app.main:app --reload