.PHONY: all build clean

all: clean build

HANDLER ?= api
LAMBDA_DIR = lambda
PACKAGE_ZIP = lambda/$(HANDLER)-handler.zip
TEMP_DIR = /tmp/lambda-build-$(HANDLER)-$(shell date +%s)
PYTHON_VERSION = 3.13

build:
	@if [ ! -d "$(LAMBDA_DIR)/$(HANDLER)-handler" ]; then \
        echo "Error: Handler directory '$(LAMBDA_DIR)/$(HANDLER)-handler' does not exist."; \
        exit 1; \
    fi

	@echo "Building Lambda package for $(HANDLER) handler..."
	@rm -f $(PACKAGE_ZIP)
	@mkdir -p $(TEMP_DIR)

	@uv export --frozen --no-dev --no-editable -o $(LAMBDA_DIR)/requirements.txt
	@uv pip install \
		--no-installer-metadata \
		--no-compile-bytecode \
		--python-platform x86_64-manylinux2014 \
		--python 3.13 \
		--target $(TEMP_DIR) \
		-r $(LAMBDA_DIR)/requirements.txt
	
	@cp $(LAMBDA_DIR)/$(HANDLER)-handler/index.py $(TEMP_DIR)/

	@echo "Optimizing Lambda package..."
	@find $(TEMP_DIR) -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find $(TEMP_DIR) -name "*.pyc" -delete 2>/dev/null || true
	@find $(TEMP_DIR) -name "*.pyo" -delete 2>/dev/null || true
	@find $(TEMP_DIR) -name ".DS_Store" -delete 2>/dev/null || true
	@find $(TEMP_DIR) -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true
	@find $(TEMP_DIR) -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true
	@find $(TEMP_DIR) -name "pip*" -delete 2>/dev/null || true
	@find $(TEMP_DIR) -name "setuptools*" -delete 2>/dev/null || true
	@find $(TEMP_DIR) -name "wheel*" -delete 2>/dev/null || true
	
	@echo "Creating deployment package..."
	@cd $(TEMP_DIR) && zip -r $(CURDIR)/$(PACKAGE_ZIP) . -q
	@rm -rf $(TEMP_DIR)

	@PACKAGE_SIZE=$$(du -h $(PACKAGE_ZIP) | cut -f1); \
	echo "Lambda package created: $(PACKAGE_ZIP)"; \
	echo "Package size: $$PACKAGE_SIZE"

	@PACKAGE_SIZE_MB=$$(du -m $(PACKAGE_ZIP) | cut -f1); \
	if [ "$$PACKAGE_SIZE_MB" -gt 50 ]; then \
		echo "Warning: Package size exceeds 50MB, consider optimizing dependencies"; \
	fi

clean:
	@echo "Cleaning build artifacts..."
	@rm -f $(PACKAGE_ZIP)
	@rm -rf cdk.out/
