# ***********************
# ***********************
# GMV-SES DEIN Builder
# ***********************
# ***********************

PROJECT_NAMESPACE = gmv-bda
PROJECT_NAME = ai-service-ui

IMAGE_NAMESPACE = gmv-bda
IMAGE_NAME = ai-service-ui
IMAGE_VERSION.develop = latest_develop
IMAGE_VERSION.master = $(shell make version)
IMAGE_VERSION = $(or ${IMAGE_VERSION.${BRANCH_NAME}}, latest)

# ***********************
# ***********************
# Tools configuration
# ***********************
# ***********************

# ** Python
PYTHON_VERSION ?= python3.8
PYTHON ?= $(if $(PYTHON_VERSION),"$(shell which $(PYTHON_VERSION))","$(shell which python)")

# ** Requirements
REQ_DIR = requirements
REQ_ACTIVATE ?=
REQS = $(if $(REQ_ACTIVATE),-r $(REQ_DIR)/requirements_dev.txt,-r $(REQ_DIR)/requirements_dev.txt -r $(REQ_DIR)/requirements.txt )

# ** Virtualenv
VENV_NAME ?= venv
VENV_BIN_ACTIVATE ?= true
VENV_PATH = $(if $(VENV_BIN_ACTIVATE),$(VENV_NAME)/bin/activate,$(VENV_NAME)/Scripts/activate)
VENV_ACTIVATE ?= .
VENV_ACTIVATE += $(VENV_PATH)

# ** Setuptools
SETUP = $(VENV_ACTIVATE) && python setup.py

# ** Tox
TOX = $(VENV_ACTIVATE) && tox

# ** Bump2Version
BUMP = $(VENV_ACTIVATE) && bump2version

# ** Twine
TWINE = $(VENV_ACTIVATE) && twine

# ** Sonar
SONAR_OPTS ?=
SONAR = $(if $(SONAR_HOME),$(SONAR_HOME)/bin/sonar-scanner,sonar-scanner)
SONAR += $(if $(SONAR_OPTS),$(SONAR_OPTS),)

# ** Docker
DOCKERFILE ?= docker/Dockerfile
DOCKER_LOGIN ?= docker login -u $(DOCKER_CREDS_USR) -p $(DOCKER_CREDS_PSW) $(DOCKER_REPO)
DOCKER_REPO ?= dev-tools.labs.gmv.com:5000

# ** Jelastic
JELASTIC_ENV_NAME =
JELASTIC_ENV_NODE.develop = Server node in Jelastic
JELASTIC_ENV_NODE.master =
JELASTIC_ENV_NODE = $(or ${JELASTIC_ENV_NODE.${BRANCH_NAME}}, Server node in Jelastic)
JELASTIC_DEPLOY = docker/jelastic/jelastic_redeploy.sh
JELASTIC_CMD = docker/jelastic/jelastic_cmd.sh
JELASTIC_COMMAND = '[{ \"command\": \"pip3 install\", \"params\": \"some_packages\" }]'

# ***********************
# ***********************
# Makefile targets
# ***********************
# ***********************

help: ## Print this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

version: ## Obtain current (or BRANCH) version number
ifdef BRANCH
ifneq ($(shell git fetch --all 2>&1 >/dev/null && git rev-parse --verify --quiet $(BRANCH)),)
	@git show $(BRANCH):setup.cfg | grep '^current_version' | sed -r s,"^.*=\s*",,
else
	@echo "ERROR: Not exists branch '$(BRANCH)'"
endif
else
	@grep '^current_version' setup.cfg | sed -r s,"^.*=\s*",,
endif

security: ## Scan for security issues
	$(TOX) -e security

licenses: ## List software license of Python packages
	$(TOX) -e licenses

install: ## Install python package
	$(SETUP) build install

.SILENT: clean clean_platform clean_venv install

clean_platform:	## Remove files that clash across platforms
	rm -f *.so */*.so
	rm -f *.pyc */*.pyc */*/*.pyc */*/*/*.pyc */*/*/*/*.pyc */*/*/*/*/*.pyc
	rm -f *.pyo */*.pyo */*/*.pyo */*/*/*.pyo */*/*/*/*.pyo */*/*/*/*/*.pyo
	rm -f *.pyd */*.pyd */*/*.pyd */*/*/*.pyd */*/*/*/*.pyd */*/*/*/*/*.pyd
	rm -rf __pycache__ */__pycache__ */*/__pycache__ */*/*/__pycache__ */*/*/*/__pycache__ */*/*/*/*/__pycache__
	rm -rf .eggs */.eggs */*/.eggs */*/*/.eggs */*/*/*/.eggs */*/*/*/*/.eggs
	rm -rf *.egg-info */.egg-info */*/*.egg-info */*/*/*.egg-info */*/*/*/*.egg-info */*/*/*/*/*.egg-info

clean: clean_platform	## Remove artifacts of test, execution, installation, etc
	rm -f *$$py.class */*$$py.class */*/*$$py.class */*/*/*$$py.class */*/*/*/*$$py.class */*/*/*/*/*$$py.class
	rm -f */.db */*/.db */*/*/.db */*/*/*/.db */*/*/*/*/.db */*/*/*/*/*/.db
	rm -f */.coverage */*/.coverage */*/*/.coverage */*/*/*/.coverage */*/*/*/*/.coverage */*/*/*/*/*/.coverage
	rm -f setuptools-*.egg distribute-*.egg distribute-*.tar.gz
	rm -rf coverage/* cover .coverage .coverage.* coverage.egg-info
	rm -rf build dist htmlcov .tox .mypy_cache
	rm -rf tests/eggsrc/build tests/eggsrc/dist tests/eggsrc/*.egg-info
	rm -rf doc/_build doc/_spell doc/sample_html_beta
	rm -rf .cache .pytest_cache .hypothesis

clean_venv:	## Remove virtual environment
	if [ -d $(VENV_NAME) ]; then rm -rf $(VENV_NAME); fi

venv: $(VENV_PATH)	## Create virtual environment
$(VENV_PATH):
	@echo "[$@] Create environment in $(VENV_NAME)"
	test -d $(VENV_NAME) || $(PYTHON) -m venv $(VENV_NAME)
	@echo "[$@] Install requirements in $(VENV_NAME)"
	$(VENV_ACTIVATE) && pip install --upgrade pip~=22.0.3 && python -m pip --timeout 100 install $(REQS) pip-tools==6.5.1 && pre-commit install
	touch $(VENV_PATH)

build: venv ## Build the project
	@echo  "[$@] Building project with version number $(shell make version)"
	$(SETUP) clean --all build sdist --format=zip bdist_wheel

test: venv ## Run unit test
	@echo "[$@] Running Unit test"
	# $(TOX)

qa: venv ## Run quality analysis
	@echo "[$@] Running SonarQube analysis"
	$(SONAR)

e2e: venv ## Run e2e test
	@echo "[$@] Running E2E test"

publish: clean venv ## Publish the project
	@echo  "[$@] Publishing project with version number $(shell make version)"
	$(SETUP) sdist --format=gztar,zip bdist_wheel
	$(TWINE) upload -r dein dist/*

archive: ## Archive docker image
	$(call check_defined, BRANCH_NAME, Required parameter missing)
	@echo "[$@] Archiving docker image with version number $(IMAGE_VERSION)"
	@make docker-deploy IMAGE_VERSION=$(IMAGE_VERSION)

deploy: ## Deploy in Jelastic
	$(call check_defined, BRANCH_NAME, Required parameter missing)
	@echo "[$@] Deploying in Jelastic"
	@$(JELASTIC_DEPLOY) $(CONTINUUM_JELASTIC_USR) $(CONTINUUM_JELASTIC_PSW) $(JELASTIC_ENV_NAME) $(JELASTIC_ENV_NODE) $(IMAGE_VERSION)
doc-build: ## Build doc
	@echo "[$@] Install pitia-libs"
	$(VENV_ACTIVATE) && pip install dist/*.whl --timeout 3600 --default-timeout 3600 
	@echo "[$@] Install requirements_doc in $(VENV_NAME)"
	$(VENV_ACTIVATE) && pip install -r $(REQ_DIR)/requirements_doc.txt --timeout 3600 --default-timeout 3600 
	@echo "[$@] Build doc"
	$(VENV_ACTIVATE) && cd docs && make clean latexpdf
	$(VENV_ACTIVATE) && cd docs && make html

	
.PHONY : help version security licenses install venv clean build test publish archive deploy

# ***********************
# ***********************
# Git functions
# ***********************
# ***********************

release-start: venv ## Create a new release with parameters RELEASE_VERSION && RELEASE_DEVELOP_VERSION
	$(call check_defined, RELEASE_VERSION, Required parameter missing)
	$(call check_defined, RELEASE_DEVELOP_VERSION, Required parameter missing)
	@echo "[$@] Starting the release $(RELEASE_VERSION)"
	@git checkout -b release/$(RELEASE_VERSION) develop
	@git checkout develop
	@$(BUMP) --new-version=$(RELEASE_DEVELOP_VERSION) minor
	@git checkout release/$(RELEASE_VERSION)
	@git push origin --all -u

release-finish: venv ## Finish a current hotfix branch
	@$(eval RELEASE_VERSION := $(shell git for-each-ref --format="%(refname:short)" refs/heads/release | tail -1 | sed 's/release\///g'))
	@$(eval RELEASE_DEVELOP_VERSION := $(shell make version BRANCH=develop))
	@echo "[$@] Finish release $(RELEASE_VERSION)"
	@git checkout develop
	@$(BUMP) --new-version=$(RELEASE_VERSION) release
	@git checkout release/$(RELEASE_VERSION)
	@$(BUMP) --new-version=$(RELEASE_VERSION) release
	@git checkout master
	@git merge --no-ff release/$(RELEASE_VERSION) -m "Merge release/$(RELEASE_VERSION) into master"
	@git tag -a $(RELEASE_VERSION) -m "Tag release $(RELEASE_VERSION)"
	@make publish
	@git checkout develop
	@git merge --no-ff release/$(RELEASE_VERSION) -m "Merge release/$(RELEASE_VERSION) into develop"
	@$(BUMP) --new-version=$(RELEASE_DEVELOP_VERSION) minor
	@git push origin --all -u
	@git push --tags
	@git branch -D release/$(RELEASE_VERSION)
	@git push origin -d -f release/$(RELEASE_VERSION)
	@echo "[$@] Release $(RELEASE_VERSION) finished."

hotfix-start: venv ## Create a new hotfix branch with parameter RELEASE_VERSION
	$(call check_defined, RELEASE_VERSION, Required parameter missing)
	@echo "[$@] Starting the hotfix $(RELEASE_VERSION)"
	@git checkout -b hotfix/$(RELEASE_VERSION) master
	@$(BUMP) --new-version=$(RELEASE_VERSION).dev patch
	@git push origin --all -u

hotfix-finish: venv ## Finish a current hotfix branch
	@$(eval RELEASE_VERSION := $(shell git for-each-ref --format="%(refname:short)" refs/heads/hotfix | tail -1 | sed 's/hotfix\///g'))
	@$(eval RELEASE_DEVELOP_VERSION := $(shell make version BRANCH=develop))
	@echo  "[$@] Finishing hotfix $(RELEASE_VERSION)"
	@git checkout develop
	@$(BUMP) --new-version=$(RELEASE_VERSION) release
	@git checkout hotfix/$(RELEASE_VERSION)
	@$(BUMP) --new-version=$(RELEASE_VERSION) release
	@git checkout master
	@git merge --no-ff hotfix/$(RELEASE_VERSION) -m "Merge hotfix/$(RELEASE_VERSION) into master"
	@git tag -a $(RELEASE_VERSION) -m "Tag hotfix $(RELEASE_VERSION)"
	@make publish
	@git checkout develop
	@git merge --no-ff hotfix/$(RELEASE_VERSION) -m "Merge hotfix/$(RELEASE_VERSION) into develop"
	@$(BUMP) --new-version=$(RELEASE_DEVELOP_VERSION) minor
	@git push origin --all -u
	@git push --tags
	@git branch -D hotfix/$(RELEASE_VERSION)
	@git push origin -d -f hotfix/$(RELEASE_VERSION)
	@echo  "[$@] Hotfix $(RELEASE_VERSION) finished."

# ***********************
# ***********************
# Docker functions
# ***********************
# ***********************

docker-build: ## Build the Docker image
	@echo "[$@] Version to build: $(IMAGE_VERSION)"
	@DOCKER_BUILDKIT=1 docker build --tag $(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_VERSION) --build-arg HTTP_PROXY=$(http_proxy) --build-arg HTTPS_PROXY=$(http_proxy) --build-arg http_proxy=$(http_proxy) --build-arg https_proxy=$(http_proxy) -f $(DOCKERFILE) .
	@echo "[$@] Docker image built $(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_VERSION)"

docker-deploy: ## Deploy the Docker image
	@eval $(DOCKER_LOGIN)
	docker tag $(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_VERSION) $(DOCKER_REPO)/$(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_VERSION)
	docker push $(DOCKER_REPO)/$(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_VERSION)
	@echo "[$@] Docker image deployed on $(DOCKER_REPO)/$(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_VERSION)"

docker-run: ## Run the docker image locally
	docker run -d -p 5000:5000 $(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_VERSION)

# ***********************
# ***********************
# Auxiliar functions
# ***********************
# ***********************
# Check that given variables are set and all have non-empty values,
# die with an error otherwise.
#
# Params:
#   1. Variable name(s) to test.
#   2. (optional) Error message to print.
check_defined = \
	$(strip $(foreach 1,$1, \
		$(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
	$(if $(value $1),, \
		$(error Undefined $1$(if $2, ($2))))
