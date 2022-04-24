#!/bin/bash
docker-compose down --rmi all
docker-compose -f docker-compose-prod.yml up -d --build
