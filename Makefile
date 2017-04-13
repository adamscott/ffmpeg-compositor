SRC_DIR := ffmpeg_compositor
UI_DIR := $(SRC_DIR)/ui
VIEWS_GEN_DIR := $(SRC_DIR)/views/gen
VIEWS_GEN_FILES := $(addprefix $(VIEWS_GEN_DIR)/, $(addsuffix _ui.py, $(basename $(notdir $(wildcard $(UI_DIR)/*.ui)))))

PYUIC5 := pyuic5

$(VIEWS_GEN_DIR)/%_ui.py: $(UI_DIR)/%.ui
	$(PYUIC5) --from-imports $< -o $@

.PHONY: build_views_ui
build_views_ui: $(VIEWS_GEN_FILES)

all: build_views_ui

.PHONY: clean
clean: 
	rm -f $(VIEWS_GEN_FILES)