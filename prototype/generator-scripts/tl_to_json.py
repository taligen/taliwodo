#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import argparse
import re
import datetime




def add_description(step, section, description):
    if section == "id":
        step["id"] = description
    else:
        ss = step.get(section, {})
        d = ss.get("description", "")
        d += description
        ss["description"] = d
        step[section] = ss
    return step


def add_step(steps, step, section):
    if section != "":
        steps.append(step)
    return steps


def read_through_file(filename):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()

    steps = []
    step_num = 1
    step = {}

    section = ""
    for line in lines:
        if line[0] == '#':
            pass
        elif line.strip() == '':
            steps = add_step(steps, step, section)
            section = ""
            step = {"id": str(step_num)}
            step_num += 1
        else:
            linematch = re.match("([A-Za-z]+):\s(.*)", line)
            if linematch:
                section = linematch.group(1).lower()
                description = linematch.group(2)
            else:
                description = "\n"+ line
            add_description(step, section, description)
    steps = add_step(steps, step, section)
    return steps


def parse_arguments():
    argparser = argparse.ArgumentParser(description="taligen: generate json file from tl file")
    argparser.add_argument("tl_file", type=str, help=".tl (task list) file to generate from")
    return argparser.parse_args()


def main():
    args = parse_arguments()

    script = {"name": args.tl_file}
    script["generated"] = datetime.datetime.now()
    script["parameters"] = {}
    script["steps"] = read_through_file(args.tl_file)

    print(script)
    # for step in steps:
    #     print(step)




main()
 