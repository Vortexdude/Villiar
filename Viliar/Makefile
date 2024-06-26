PROJECT_NAME := $(shell basename $(CURDIR))
LOCAL_EXEC	:=	/bin/bash -c

ARGS :=
ifneq ($(port),)
ARGS += --port $(port)
endif

ifneq ($(debug),)
ARGS += --debug $(debug)
endif

ifneq ($(host),)
ARGS += --host $(host)
endif

ifneq ($(count),)
ARGS += --count $(count)
endif

all:
	$(info Intialization ${PROJECT_NAME})

start:
	@$(LOCAL_EXEC) "./scripts/docker --action $@ $(ARGS)"

restart:
	@$(LOCAL_EXEC) "./scripts/docker --action $@ $(ARGS)"

stop:
	@$(LOCAL_EXEC) "./scripts/docker --action $@ $(ARGS)"

connect:
	@$(LOCAL_EXEC) "./scripts/docker --action $@ $(ARGS)"
