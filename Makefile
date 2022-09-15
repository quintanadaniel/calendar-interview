all-tests:
	@echo "testing in folder application/tests"
	coverage run -m unittest discover -v

coverage-tests:
	@echo "testing in folder application/tests"
	coverage report -m

flask-db-init:
	echo "If it is first time execute init package migrations in the project"
	flask db init

flask-db-migrate:
	echo "Executing migrate db before apply the change"
	flask db migrate

flask-db-upgrade:
	echo "Applying the change in the data base"
	flask db upgrade

flask-db-downgrade:
	echo "Applying revert migration in the data base"
	flask db downgrade

flask-db-stamp-head:
	echo "indicate that the current state of the database represents the application of all migrations"
	flask db stamp head

######################################################
## Execute the menu to apply migrations with flask ##
#####################################################
init-db: flask-db-init

migrate-apply-db: flask-db-migrate flask-db-upgrade flask-db-stamp-head

######################################
## Execute the tests and coverage  ##
#####################################
make test-coverage: all-tests coverage-tests
