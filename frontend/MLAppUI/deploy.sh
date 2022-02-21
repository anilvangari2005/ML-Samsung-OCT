#!/bin/bash
ng build
aws s3 sync ./dist/mlapp-ui s3://samsung-oct-2-frontend --delete
