SRC_DIR				=	./src
JSON_DIR			= 	./assets/json
DETECTION_DIR		= 	$(SRC_DIR)/detection
SESSION_DIR			= 	$(SRC_DIR)/session
SPEECH_DIR			= 	$(SRC_DIR)/speech
ST_MACHINES_DIR		= 	$(SRC_DIR)/state_machines
STORAGE_MNG_DIR		= 	$(SRC_DIR)/storage_management
TESTS_DIR			=	./test
TMP_DIR				=	./tmp


COLOR				=	"\033["
GREEN				=	";32m"
CYAN				=	";36m"
PURPLE				=	";35m"
GREY				=	"1;30m"
BOLD				=	";1"
ITALIC				=	";3"
NOCOLOR				=	"\033[0m"


############################## MAIN RULES ##############################

all : initiate-camera build

build :
	@mkdir -p tmp
	@mkdir -p tmp/img
	@cd tmp/img && wget https://files.ros4.pro/reachy-mini.png

initiate-camera:
	@echo $(COLOR)$(BOLD)$(CYAN)"Starting autofocus"$(NOCOLOR)
	@cd $(DETECTION_DIR) && python3 initiate_camera.py

show-last-picture: build
	@echo $(COLOR)$(BOLD)$(CYAN)"Showing last image"$(NOCOLOR)
	@cd $(STORAGE_MNG_DIR) && python3 show_last_img.py

delete-pictures: build
	@echo $(COLOR)$(BOLD)$(CYAN)"Deleting last images"$(NOCOLOR)
	@cd $(STORAGE_MNG_DIR) && python3 delete_png.py


############################## REACHY RULES ##############################

reload_server:
	@echo $(COLOR)$(BOLD)$(CYAN)"Reloading servers"$(NOCOLOR)
	@./reload_server

reachy-final:
	@echo $(COLOR)$(BOLD)$(GREEN)"Starting reachy with final version"$(NOCOLOR)
	@cd $(ST_MACHINES_DIR) && python3 reachy_state_machine_argv.py ../../$(JSON_DIR)/state_machine_final.json

reachy-only-aruco:
	@echo $(COLOR)$(BOLD)$(GREEN)"Starting reachy with only aruco version"$(NOCOLOR)
	@cd $(ST_MACHINES_DIR) && python3 reachy_state_machine_argv.py ../../$(JSON_DIR)/state_machine_only_aruco.json

reachy-without-research:
	@echo $(COLOR)$(BOLD)$(GREEN)"Starting reachy with only aruco version"$(NOCOLOR)
	@cd $(ST_MACHINES_DIR) && python3 reachy_state_machine_argv.py ../../$(JSON_DIR)/state_machine_sans_recherche.json

reachy-test-photo:
	@echo $(COLOR)$(BOLD)$(GREEN)"Starting reachy with only aruco version"$(NOCOLOR)
	@cd $(ST_MACHINES_DIR) && python3 reachy_state_machine_argv.py ../../$(JSON_DIR)/state_machine_test_photo.json


############################## FAKE-REACHY RULES ##############################

fake-reachy-final:
	@echo $(COLOR)$(BOLD)$(GREEN)"Starting reachy with final version"$(NOCOLOR)
	@cd $(ST_MACHINES_DIR) && python3 fake_reachy_state_machine_argv.py ../../$(JSON_DIR)/state_machine_final.json

fake-reachy-only-aruco:
	@echo $(COLOR)$(BOLD)$(GREEN)"Starting reachy with only aruco version"$(NOCOLOR)
	@cd $(ST_MACHINES_DIR) && python3 fake_reachy_state_machine_argv.py ../../$(JSON_DIR)/state_machine_only_aruco.json

fake-reachy-without-research:
	@echo $(COLOR)$(BOLD)$(GREEN)"Starting reachy with only aruco version"$(NOCOLOR)
	@cd $(ST_MACHINES_DIR) && python3 fake_reachy_state_machine_argv.py ../../$(JSON_DIR)/state_machine_sans_recherche.json

fake-reachy-test-photo:
	@echo $(COLOR)$(BOLD)$(GREEN)"Starting reachy with only aruco version"$(NOCOLOR)
	@cd $(ST_MACHINES_DIR) && python3 fake_reachy_state_machine_argv.py ../../$(JSON_DIR)/state_machine_test_photo.json

clean: $(TMP_DIR)
	@echo $(COLOR)$(BOLD)$(RED)"Cleaning the tmp directory"$(NOCOLOR)
	@rm -rf $^


############################## INSTALL RULES ##############################

.PHONY: install all clean

install:
	@echo $(COLOR)$(BOLD)$(PURPLE)"Installing the libraries"$(NOCOLOR)
	@pip install -r ./requirements.txt
	@echo $(COLOR)$(BOLD)$(GREY)"Ready to work"$(NOCOLOR)

############################## TESTS RULES ##############################