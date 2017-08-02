#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import argparse
import re
import datetime
import json
import os



def add_original_description(step, section, description):
    if section == "id":
        step["id"] = description
    else:
        ss = step.get(section, {})
        d = ss.get("raw_description", "")
        d += description
        ss["raw_description"] = d
        ss["description"] = d
        step[section] = ss
    return step

def add_comment(script, step, section, comment):
    if section == "":
        c = step.get("comment", "")
        step["comment"] = c + comment
    else:
        ss = step.get(section, {})
        c = ss.get("comment", "")
        c += comment
        ss["comment"] = c
        step[section] = ss
    return step


def add_step(steps, step, section):
    if section != "" or "comment" in step or "call" in step:
        steps.append(step)
    return steps


def read_through_file(filename, script):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()

    steps = []
    step_num = 1
    step = {"id": str(step_num), "order": step_num}

    section = ""
    for line in lines:
        if line[0] == '#':
            add_comment(script, step, section, line)
        elif line.strip() == '':
            steps = add_step(steps, step, section)
            if section != "" or "comment" in step:
                step_num += 1
                step = {"id": str(step_num), "order": step_num}
            section = ""
        else:
            last_section = section
            linematch = re.match("([A-Za-z]+):\s*(.*)", line)
            if linematch:
                section = linematch.group(1).lower()
                description = linematch.group(2)
            else:
                description = "\n"+ line
            if linematch and section == "call":
                steps = add_step(steps, step, last_section)

                if last_section != "" or "comment" in step:
                    step_num += 1
                    step = {"id": str(step_num), "order": step_num}
                section = ""
                step["call"] = linematch.group(2)
                call_file_match = re.match("(.+)\((.*)\)\s*", linematch.group(2))
                call_file = call_file_match.group(1) + ".tl"
                step["name"] = call_file
                step["parameters"] = call_file_match.group(2).strip()
                step["steps"] = read_through_file(call_file, step)
                steps = add_step(steps, step, section)

                step_num += 1
                step = {"id": str(step_num), "order": step_num}
            else:
                add_original_description(step, section, description)
    steps = add_step(steps, step, section)
    return steps


def parse_arguments():
    argparser = argparse.ArgumentParser(description="taligen: generate json file from tl file")
    argparser.add_argument("tl_file", type=str, help=".tl (task list) file to generate from")
    return argparser.parse_args()


def main():
    args = parse_arguments()

    script = {"name": args.tl_file}
    script["generated"] = str(datetime.datetime.now())
    script["parameters"] = {}
    script["steps"] = read_through_file(args.tl_file, script)

    dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    with open(dt+"."+os.path.splitext(args.tl_file)[0]+'.json', 'w') as fp:
        json.dump(script, fp, sort_keys=True, indent=4)




main()
 