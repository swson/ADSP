HPCG=hpcg-3.1
HPCG_BUILD=$(HPCG)/build
HPCG_BIN=$(HPCG_BUILD)/bin/xhpcg
PMU=libpmu

# Build all components
all: pmu hpcg

# Build PMU
pmu:
	sudo make CC=g++ -C $(PMU) install
	sudo make -C $(PMU) kernel

# Build HPCG
hpcg:
	mkdir -p $(HPCG_BUILD)
	cd $(HPCG_BUILD) && ../configure Linux_Serial && make

# Clean only compiled objects safely
clean:
	$(MAKE) -C $(PMU) clean || true
	[ -d "$(HPCG_BUILD)" ] && $(MAKE) -C $(HPCG_BUILD) clean || true

# Optional: Deep clean (with backup notice)
deep-clean:
	@echo "WARNING: This will delete the entire hpcg-3.1 and libpmu directories!"
	@read -p "Proceed? (y/N): " confirm; \
	if [ "$$confirm" = "y" ]; then \
		rm -rf $(HPCG) $(PMU); \
	else \
		echo "Aborted."; \
	fi
