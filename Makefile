.PHONY: auth run

auth:
	@echo "Authenticating with Google API..."
	pipenv run python auth.py

run: auth
	@echo "Running the main application..."
	pipenv run python main.py

deploy: auth
	@echo "Deploying the application to lambda"
	bash deploy_to_lambda.sh