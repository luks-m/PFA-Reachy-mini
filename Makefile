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

NB_PHOTOS			?= 100
NB_TO_DELETE		?= 2


############################## MAIN RULES ##############################

all : initiate-camera build

build :
	@mkdir -p tmp
	@mkdir -p tmp/img
	@cd tmp/img && wget https://files.ros4.pro/reachy-mini.png


############################## INSTALL RULES ##############################

.PHONY: install all clean

install:
	@echo $(COLOR)$(BOLD)$(PURPLE)"Installing the libraries"$(NOCOLOR)
	@pip install -r ./requirements.txt
	@echo $(COLOR)$(BOLD)$(GREY)"Ready to work"$(NOCOLOR)


############################## INITIALISATION RULES ##############################

initiate-camera:
	@echo $(COLOR)$(BOLD)$(CYAN)"Starting autofocus"$(NOCOLOR)
	@cd $(DETECTION_DIR) && python3 initiate_camera.py

show-last-picture: build
	@echo $(COLOR)$(BOLD)$(CYAN)"Showing last image"$(NOCOLOR)
	@cd $(STORAGE_MNG_DIR) && python3 show_last_img.py

delete-pictures: build
	@echo $(COLOR)$(BOLD)$(CYAN)"Deleting oldest images"$(NOCOLOR)
	@cd $(STORAGE_MNG_DIR) && python3 delete_images.py ${NB_PHOTOS} ${NB_TO_DELETE}


############################## REACHY RULES ##############################

reload_server:
	@echo $(COLOR)$(BOLD)$(CYAN)"Reloading servers"$(NOCOLOR)
	@./reload_server.sh

reachy-final:
	@echo $(COLOR)$(BOLD)$(GREEN)"Starting reachy with final version"$(NOCOLOR)
	@cd $(ST_MACHINES_DIR) && python3 reachy_state_machine_argv.py ../../$(JSON_DIR)/state_machine_final.json

reachy-only-aruco:
	@echo $(COLOR)$(BOLD)$(GREEN)"Starting reachy with only aruco version"$(NOCOLOR)
	@cd $(ST_MACHINES_DIR) && python3 reachy_state_machine_argv.py ../../$(JSON_DIR)/state_machine_only_aruco.json


############################## FAKE-REACHY RULES ##############################

fake-reachy-final:
	@echo $(COLOR)$(BOLD)$(GREEN)"Starting reachy with final version"$(NOCOLOR)
	@cd $(ST_MACHINES_DIR) && python3 fake_reachy_state_machine_argv.py ../../$(JSON_DIR)/state_machine_final.json

fake-reachy-only-aruco:
	@echo $(COLOR)$(BOLD)$(GREEN)"Starting reachy with only aruco version"$(NOCOLOR)
	@cd $(ST_MACHINES_DIR) && python3 fake_reachy_state_machine_argv.py ../../$(JSON_DIR)/state_machine_only_aruco.json


############################## CLEANING RULES ##############################

clean: $(TMP_DIR)
	@echo $(COLOR)$(BOLD)$(RED)"Cleaning the imported images"$(NOCOLOR)
	@rm -rf $(TMP_DIR)/img/reachy*

clean-all: $(TMP_DIR)
	@echo $(COLOR)$(BOLD)$(RED)"Cleaning the tmp directory"$(NOCOLOR)
	@rm -rf $^