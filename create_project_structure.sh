#!/bin/bash

# Set the project root directory name
PROJECT_ROOT="project_root"

# Create the base directory
mkdir -p $PROJECT_ROOT

# Create main app structure
mkdir -p $PROJECT_ROOT/app/models
mkdir -p $PROJECT_ROOT/app/schemas
mkdir -p $PROJECT_ROOT/app/routers
mkdir -p $PROJECT_ROOT/app/services
mkdir -p $PROJECT_ROOT/app/utils
mkdir -p $PROJECT_ROOT/app/tests

# Create migrations directory
mkdir -p $PROJECT_ROOT/migrations/versions

# Create necessary files
touch $PROJECT_ROOT/app/__init__.py
touch $PROJECT_ROOT/app/main.py
touch $PROJECT_ROOT/app/config.py
touch $PROJECT_ROOT/app/dependencies.py
touch $PROJECT_ROOT/app/db.py
touch $PROJECT_ROOT/app/auth.py
touch $PROJECT_ROOT/app/llm.py

# Create model files
touch $PROJECT_ROOT/app/models/__init__.py
touch $PROJECT_ROOT/app/models/user.py
touch $PROJECT_ROOT/app/models/market.py
touch $PROJECT_ROOT/app/models/customer.py
touch $PROJECT_ROOT/app/models/competitor.py
touch $PROJECT_ROOT/app/models/product.py
touch $PROJECT_ROOT/app/models/expansion.py

# Create schema files
touch $PROJECT_ROOT/app/schemas/__init__.py
touch $PROJECT_ROOT/app/schemas/user.py
touch $PROJECT_ROOT/app/schemas/market.py
touch $PROJECT_ROOT/app/schemas/customer.py
touch $PROJECT_ROOT/app/schemas/competitor.py
touch $PROJECT_ROOT/app/schemas/product.py
touch $PROJECT_ROOT/app/schemas/expansion.py

# Create router files
touch $PROJECT_ROOT/app/routers/__init__.py
touch $PROJECT_ROOT/app/routers/users.py
touch $PROJECT_ROOT/app/routers/market_analysis.py
touch $PROJECT_ROOT/app/routers/customer_discovery.py
touch $PROJECT_ROOT/app/routers/competitive_intelligence.py
touch $PROJECT_ROOT/app/routers/product_evolution.py
touch $PROJECT_ROOT/app/routers/market_expansion.py

# Create service files
touch $PROJECT_ROOT/app/services/__init__.py
touch $PROJECT_ROOT/app/services/user_service.py
touch $PROJECT_ROOT/app/services/market_service.py
touch $PROJECT_ROOT/app/services/customer_service.py
touch $PROJECT_ROOT/app/services/competitor_service.py
touch $PROJECT_ROOT/app/services/product_service.py
touch $PROJECT_ROOT/app/services/expansion_service.py

# Create utility files
touch $PROJECT_ROOT/app/utils/__init__.py
touch $PROJECT_ROOT/app/utils/logger.py
touch $PROJECT_ROOT/app/utils/helpers.py

# Create test files
touch $PROJECT_ROOT/app/tests/__init__.py
touch $PROJECT_ROOT/app/tests/test_users.py
touch $PROJECT_ROOT/app/tests/test_market.py
touch $PROJECT_ROOT/app/tests/test_customer.py
touch $PROJECT_ROOT/app/tests/test_competitor.py
touch $PROJECT_ROOT/app/tests/test_product.py
touch $PROJECT_ROOT/app/tests/test_expansion.py

# Create migrations files
touch $PROJECT_ROOT/migrations/env.py
touch $PROJECT_ROOT/migrations/script.py.mako
touch $PROJECT_ROOT/migrations/alembic.ini

# Create project root files
touch $PROJECT_ROOT/.env
touch $PROJECT_ROOT/.gitignore
touch $PROJECT_ROOT/requirements.txt
touch $PROJECT_ROOT/README.md
touch $PROJECT_ROOT/Dockerfile
touch $PROJECT_ROOT/docker-compose.yml

# Print success message
echo "Project folder structure created successfully in $PROJECT_ROOT"
