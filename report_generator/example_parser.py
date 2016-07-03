#!/usr/bin/python
import os, re, yaml

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))
COMPILER = [
    "armgcc",
    "atl",
    "iar",
    "kds",
    "mdk",
]

def parse_examples(boards = None, repo = REPO):
    """
        parse yml file to get available demo_apps/driver_examples
        structure:
        BOARD:
            SOC
            DEMO_APP:
                COMPILER: STATUS
                ...
    """
    records_dir = os.path.join(repo, 'bin\\generator\\records')
    sdk_examples_dir = os.path.join(records_dir, 'ksdk\\sdk_example')
    usb_examples_dir = os.path.join(records_dir, 'ksdk\\usb_example')
    demo_app_lib = os.path.join(sdk_examples_dir, "common\\demo_app.yml")
    driver_example_lib = os.path.join(sdk_examples_dir, "common\\driver_example.yml")

    demo_app_result = {}
    driver_example_result = {}
    usb_result = {}

    # list of all demo_app
    with open(demo_app_lib, 'r') as stream:
        demo_app = yaml.load(stream)
    # list of all driver_example
    with open(driver_example_lib, 'r') as stream:
        driver_example = yaml.load(stream)
    # list of all usb example
    usb_example = []
    for _file in os.listdir(os.path.join(usb_examples_dir, "common")):
        if not _file.endswith(".yml"):
            continue
        with open(os.path.join(usb_examples_dir, "common", _file), 'r') as stream:
            cur = yaml.load(stream)
            if not "__load__" in cur:
                continue
            for _path in cur["__load__"]:
                if ("usb_example_common.yml" in _path) or (not r"ksdk\usb_example\common" in _path):
                    continue
                usb_example.append(os.path.basename(_path).replace(".yml", ""))
    boards.sort()
    # print "loading drivers/demos/examples"
    for board in boards:
        board = board.replace('-','').lower()
        demo_app_result[board] = {}
        driver_example_result[board] = {}
        usb_result[board] = {}

        # get soc
        if not ('%s.yml' % board) in os.listdir(os.path.join(records_dir, 'ksdk\\options')):
            continue
        with open(os.path.join(records_dir, 'ksdk\\options\\%s.yml' % board), 'r') as stream:
            board_option = yaml.load(stream)
            demo_app_result[board]["soc"] = board_option["__variable__"]["soc"]
            driver_example_result[board]["soc"] = board_option["__variable__"]["soc"]
            usb_result[board]["soc"] = board_option["__variable__"]["soc"]

        with open(os.path.join(sdk_examples_dir, '%s.yml' % board), 'r') as stream:
            board_demo_example = yaml.load(stream)
            # get demo_app
            # filter by compiler
            for demo in demo_app:
                if demo == "__hierarchy__":
                    continue
                demo_app_result[board][demo] = {}
                for compiler in COMPILER:
                    demo_app_result[board][demo][compiler] = None
                    if not demo in board_demo_example:
                        continue
                    if not board_demo_example[demo]:
                        continue
                    if not "attribute" in board_demo_example[demo]:
                        continue
                    if (not "configuration" in board_demo_example[demo]) and ("attribute" in board_demo_example[demo]):
                        demo_app_result[board][demo][compiler] = board_demo_example[demo]["attribute"].replace("required", "A")
                        continue
                    if not "tools" in board_demo_example[demo]["configuration"]:
                        continue
                    if not "__remove__" in board_demo_example[demo]["configuration"]["tools"]:
                        if not compiler in board_demo_example[demo]["configuration"]["tools"]:
                            demo_app_result[board][demo][compiler] = board_demo_example[demo]["attribute"].replace("required", "A")
                        elif not "config" in board_demo_example[demo]["configuration"]["tools"][compiler]:
                            demo_app_result[board][demo][compiler] = board_demo_example[demo]["attribute"].replace("required", "A")
                        elif not "__remove__" in board_demo_example[demo]["configuration"]["tools"][compiler]["config"]:
                            demo_app_result[board][demo][compiler] = board_demo_example[demo]["attribute"].replace("required", "A")
                        else:
                            if "debug" in board_demo_example[demo]["configuration"]["tools"][compiler]["config"]["__remove__"]:
                                demo_app_result[board][demo][compiler] = "Ro"
                            if "release" in board_demo_example[demo]["configuration"]["tools"][compiler]["config"]["__remove__"]:
                                demo_app_result[board][demo][compiler] = "Do"
                        continue
                    if not compiler in board_demo_example[demo]["configuration"]["tools"]["__remove__"]:
                        demo_app_result[board][demo][compiler] = board_demo_example[demo]["attribute"].replace("required", "A")
                        continue
                    else:
                        demo_app_result[board][demo][compiler] = board_demo_example[demo]["attribute"].replace("required", "A")
                        continue

            #get driver_example
            for example in driver_example:
                if example == "__hierarchy__":
                    continue
                driver_example_result[board][example] = {}
                for compiler in COMPILER:
                    driver_example_result[board][example][compiler] = None
                    if not example in board_demo_example:
                        continue
                    if not board_demo_example[example]:
                        continue
                    if not "attribute" in board_demo_example[example]:
                        continue
                    if (not "configuration" in board_demo_example[example]) and ("attribute" in board_demo_example[example]):
                        driver_example_result[board][example][compiler] = board_demo_example[example]["attribute"].replace("required", "A")
                        continue
                    if not "tools" in board_demo_example[example]["configuration"]:
                        continue
                    if not "__remove__" in board_demo_example[example]["configuration"]["tools"]:
                        if not compiler in board_demo_example[example]["configuration"]["tools"]:
                            driver_example_result[board][example][compiler] = board_demo_example[example]["attribute"].replace("required", "A")
                        elif not board_demo_example[example]["configuration"]["tools"][compiler]:
                            driver_example_result[board][example][compiler] = board_demo_example[example]["attribute"].replace("required", "A")
                        elif not "config" in board_demo_example[example]["configuration"]["tools"][compiler]:
                            driver_example_result[board][example][compiler] = board_demo_example[example]["attribute"].replace("required", "A")
                        elif not "__remove__" in board_demo_example[example]["configuration"]["tools"][compiler]["config"]:
                            driver_example_result[board][example][compiler] = board_demo_example[example]["attribute"].replace("required", "A")
                        else:
                            if "debug" in board_demo_example[example]["configuration"]["tools"][compiler]["config"]["__remove__"]:
                                driver_example_result[board][example][compiler] = "Ro"
                            if "release" in board_demo_example[example]["configuration"]["tools"][compiler]["config"]["__remove__"]:
                                driver_example_result[board][example][compiler] = "Do"
                        continue
                    if not compiler in board_demo_example[example]["configuration"]["tools"]["__remove__"]:
                        driver_example_result[board][example][compiler] = board_demo_example[example]["attribute"].replace("required", "A")
                        continue
                    else:
                        driver_example_result[board][example][compiler] = board_demo_example[example]["attribute"].replace("required", "A")
                        continue

        # get usb_example
        for _usb in usb_example:
            name_split = _usb.split("_")
            rtos = name_split[-1]
            usb_type = name_split[0]
            if usb_type == "dev":
                usb_type = "device"
            elif usb_type == "pin":
                usb_type = "_".join(name_split[0:2])
            usb_result[board][_usb] = {}
            target_lib = os.path.join(usb_examples_dir, board, "usb_%s_example_%s.yml" % (usb_type, rtos))
            if not os.path.isfile(target_lib):
                continue
            with open(target_lib, 'r') as stream:
                loaded_lib = yaml.load(stream)
                for compiler in COMPILER:
                    usb_result[board][_usb][compiler] = None
                    if not _usb in loaded_lib:
                        continue
                    if not "attribute" in loaded_lib[_usb]:
                        continue
                    if (not "configuration" in loaded_lib[_usb]) and ("attribute" in loaded_lib[_usb]):
                        usb_result[board][_usb][compiler] = loaded_lib[_usb]["attribute"].replace("required", "A")
                        continue
                    if not "tools" in loaded_lib[_usb]["configuration"]:
                        continue
                    if not "__remove__" in loaded_lib[_usb]["configuration"]["tools"]:
                        if not compiler in loaded_lib[_usb]["configuration"]["tools"]:
                            usb_result[board][_usb][compiler] = loaded_lib[_usb]["attribute"].replace("required", "A")
                        elif not "config" in loaded_lib[_usb]["configuration"]["tools"][compiler]:
                            usb_result[board][_usb][compiler] = loaded_lib[_usb]["attribute"].replace("required", "A")
                        elif not "__remove__" in loaded_lib[_usb]["configuration"]["tools"][compiler]["config"]:
                            usb_result[board][_usb][compiler] = loaded_lib[_usb]["attribute"].replace("required", "A")
                        else:
                            if "debug" in loaded_lib[_usb]["configuration"]["tools"][compiler]["config"]["__remove__"]:
                                usb_result[board][_usb][compiler] = "Ro"
                            if "release" in loaded_lib[_usb]["configuration"]["tools"][compiler]["config"]["__remove__"]:
                                usb_result[board][_usb][compiler] = "Do"
                        continue
                    if not compiler in loaded_lib[_usb]["configuration"]["tools"]["__remove__"]:
                        usb_result[board][_usb][compiler] = loaded_lib[_usb]["attribute"].replace("required", "A")
                        continue
                    else:
                        usb_result[board][_usb][compiler] = loaded_lib[_usb]["attribute"].replace("required", "A")
                        continue

    return (demo_app_result,
            driver_example_result,
            usb_result
            )

def get_driver_require(repo = REPO):
    from xml.dom import minidom
    result = {}
    for root, folders, files in os.walk(os.path.join(repo, 'platform\\drivers')):
        for _file in files:
            if not _file.endswith(".meta"):
                continue
            meta_dom = minidom.parse(os.path.join(root, _file)).documentElement
            driver = str(_file.replace(".meta", "").replace("fsl_", ""))
            result[driver] = []
            for component in meta_dom.getElementsByTagName('components')[0].getElementsByTagName('component'):
                if component.hasAttribute('description'):
                    for src_file in component.getElementsByTagName('source')[0].getElementsByTagName('files'):
                        if not src_file.hasAttribute('requires'):
                            continue
                        if "devices.modules." in src_file.getAttribute('requires'):
                            _driver = str(src_file.getAttribute('mask').replace('fsl_', ''))
                            _driver = _driver[:_driver.index('.')]
                            if not _driver in result:
                                result[_driver] = [str(src_file.getAttribute('requires').replace("devices.modules.", "")),]
                            else:
                                if not src_file.getAttribute('requires').replace("devices.modules.", "") in result[_driver]:
                                    result[_driver].append(str(src_file.getAttribute('requires').replace("devices.modules.", "")))
                    continue
                if component.hasAttribute('name'):
                    if not re.search(r'platform\.drivers\..*\.support', component.getAttribute('name')):
                        continue
                result[driver].append(str(component.getAttribute('requires').replace("devices.modules.", "")))
    return result

def get_examples_module(repo = REPO):
    records_dir = os.path.join(REPO, 'bin\\generator\\records')
    sdk_examples_dir = os.path.join(records_dir, 'ksdk\\sdk_example')
    usb_examples_dir = os.path.join(records_dir, 'ksdk\\usb_example')
    demo_app_lib = os.path.join(sdk_examples_dir, "common\\demo_app.yml")
    driver_example_lib = os.path.join(sdk_examples_dir, "common\\driver_example.yml")

    demo_app_result = {}
    driver_example_result = {}
    usb_result = {}

    DONT_CHECK = [
                r"port",
                r"demo",
                r"example",
                r"pinset",
                r"clock",
                r"sim",
                r"erpc",
                r"open\-amp",
                r"rtos",
                r"ucos",
                r"device",
                r"emvl1",
                ]

    # list of all demo_app
    with open(demo_app_lib, 'r') as stream:
        demo_app = yaml.load(stream)

    for demo in demo_app:
        if demo == "__hierarchy__":
            continue
        demo_app_result[demo] = []
        for module in demo_app[demo]["modules"].keys():
            if module in demo_app[demo]:
                continue
            if re.search(r'|'.join(DONT_CHECK + [demo]), module):
                continue
            if '_' in module:
                demo_app_result[demo].append(module[:module.index('_')])
            else:
                demo_app_result[demo].append(module)

    for demo in demo_app_result:
        for module in demo_app_result[demo]:
            if module in demo_app_result:
                demo_app_result[demo].remove(module)
                demo_app_result[demo] += demo_app_result[module]
        demo_app_result[demo] = sorted(list(set(demo_app_result[demo])))

    # print "finish get demos"
    # list of all driver_example
    with open(driver_example_lib, 'r') as stream:
        driver_example = yaml.load(stream)

    for example in driver_example:
        if example == "__hierarchy__":
            continue
        driver_example_result[example] = []
        for module in driver_example[example]["modules"].keys():
            if module in driver_example[example]:
                continue
            if re.search(r'|'.join(DONT_CHECK + [example]), module):
                continue
            if '_' in module:
                driver_example_result[example].append(module[:module.index('_')])
            else:
                driver_example_result[example].append(module)

    for example in driver_example_result:
        for module in driver_example_result[example]:
            if module in driver_example_result:
                driver_example_result[example].remove(module)
                driver_example_result[example] += driver_example_result[module]
        driver_example_result[example] = sorted(list(set(driver_example_result[example])))

    # print "finish get driver examples"
    # list of all usb example
    usb_lib = [
        "osa",
        "host",
        "device",
        "keyboard2mouse",
        "dev_",
        "emvl1",
        "port",
        "rtos",
        "ucos",
    ]
    for _file in os.listdir(os.path.join(usb_examples_dir, "common")):
        if not _file.endswith(".yml"):
            continue
        with open(os.path.join(usb_examples_dir, "common", _file), 'r') as stream:
            cur = yaml.load(stream)
        if not "__load__" in cur:
            continue
        for _path in cur["__load__"]:
            if ("usb_example_common.yml" in _path) or (not r"ksdk\usb_example\common" in _path):
                continue
            example = os.path.basename(_path).replace(".yml", "")
            usb_result[example] = []
            with open(os.path.join(records_dir, _path), 'r') as stream:
                _cur = yaml.load(stream)
                for module in _cur[example]["modules"]:
                    if module in usb_result[example]:
                        continue
                    if re.search('|'.join(usb_lib+[example]), module):
                        continue
                    if '_' in module:
                        usb_result[example].append(module[:module.index('_')])
                    else:
                        usb_result[example].append(module)

    for example in usb_result:
        for module in usb_result[example]:
            if module in usb_result:
                usb_result[example].remove(module)
                usb_result[example] += usb_result[module]
        usb_result[example] = sorted(list(set(usb_result[example])))

    # print "finish get usb"

    return (demo_app_result,
            driver_example_result,
            usb_result
            )

if "__main__" == __name__:
    # demo_app, driver_example, usb = get_examples_module()
    # print yaml.dump(demo_app, default_flow_style=False)
    # print yaml.dump(driver_example, default_flow_style=False)
    # print yaml.dump(usb, default_flow_style=False)
    # driver = get_driver_require()
    # print yaml.dump(driver, default_flow_style=False)
    demo_app, driver_example, usb = parse_examples(["twrke18f150m"])
    print yaml.dump(demo_app, default_flow_style=False)
    # print yaml.dump(driver_example, default_flow_style=False)
    # print yaml.dump(usb, default_flow_style=False)