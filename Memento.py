import re
from random import shuffle, getrandbits
import os
from multimethod import multimethod
from dataclasses import dataclass



INNER_FAMILY = 0b1
SECOND_INNER_FAMILY = 0b11

MEMORIZING_SEQUENCE = 0b1000

SPECIAL_FAMILY_TYPE = ("Selection", "_SELECTION")
INDENT = "    "




# data structure

# data (folder)
# └ domain1 (folder)
#   └ phylum1 (.txt file)
#     └ family1
#       ├ genus1
#       │ └ subgenus1.1
#       ├ genus2
#       │ └ subgenus2.1
#       └ genus3
#         ├ subgenus3.1
#         └ subgenus3.2







class UnknownFamilyType(Exception):
    def __init__(self, *family_types):
        message = ", ".join(family_types)
        super().__init__(f"Unknown family type: {message}") # https://www.programiz.com/python-programming/user-defined-exception

class Category_manager:
    def __init__(self) -> None:
        self.categoryD: dict[str, str] = {}

    def add_category(self, category_name, elements):
        for element in elements:
            self.categoryD[element] = category_name

    def get_category(self, element):
        return self.categoryD[element]

    def get_all_elements(self):
        return list(self.categoryD.keys())



class Subgenus:
    def __init__(self, text: str):
        self.text = text.strip()

class Genus:
    def __init__(self, text: str):
        self.subgenusL = [Subgenus(subtext) for subtext in text.split("\n")]

class Family:
    def __init__(self, text: str):
        _raw_family_types = text.split("\n")[0]
        self.typeL = _raw_family_types[1:-1].split(", ")
        self.typeL.sort(key=lambda _type: _type not in SPECIAL_FAMILY_TYPE)
        
        self.envD = { # environmental variables
            "genus_separator": "\n",
            "first_given": "",
            "start_i": 0,
            "ignorance_of_parentheses": False,
            "suggestion": "",
            "indented_multiline_genus": False,
        }


        is_manual_genus_separator: bool = False
        if re.compile(r"\[.*\]").match(text.split("\n")[1]):
            _raw_env = text.split("\n")[1]

            self.name = text.split("\n")[2]
            _maintext = "\n".join(text.split("\n")[3:])
        else:
            _raw_env = ""
            
            self.name = text.split("\n")[1]
            _maintext = "\n".join(text.split("\n")[2:])

        _key_value_pairL = _raw_env[1:-1].split(", ")
        _appending_envD = dict(_key_value_pair.split(": ") for _key_value_pair in _key_value_pairL)
        _appending_envD = \
            {key:
                re.compile(r"\\n").sub("\n", value[1:-1])   if re.compile(r""" ".*" | '.*' """, re.VERBOSE).match(value)
                else int(value) if value.isnumeric()
                else True if value in ("True", "true")
                else False if value in ("False", "false")
                else value
            for key, value in _appending_envD.items()
            }

        self.envD.update(_appending_envD)
        
        if "genus_separator" in _appending_envD.keys():
            is_manual_genus_separator = True




        min_genus_separatorD = {
            "List": "\n\n",
            "Q&A": "\n\n",
            "Q&Q": "\n\n",
            "Q&Q&Q": "\n\n", #FIXME: Q&Q&Q&Q...
            "Selection": "\n\n\n",
        }




        if not is_manual_genus_separator:
            for family_type in self.typeL:
                if (genus_separator:=min_genus_separatorD.get(family_type)) and self.envD["genus_separator"] == "\n":
                    self.envD["genus_separator"] = genus_separator


        if self.envD["indented_multiline_genus"]:
            pre_genusL = _maintext.split(self.envD["genus_separator"])
            genusL: list[Genus] = []
            for pre_genus in pre_genusL:
                if pre_genus.strip():
                    if re.match(rf"^{INDENT*2}", pre_genus): #FIXME: the condition have to be relative to other lines; not absolute `INDENT*2`
                        genusL[-1].subgenusL[-1].text += " " + pre_genus.strip()
                    else:
                        genusL.append(Genus(pre_genus.strip()))
        else:
            genusL = [Genus(pre_genus.strip()) for pre_genus in _maintext.split(self.envD["genus_separator"]) if pre_genus.strip()]

        if re.match(r"^genus\[\d+\]$", self.envD["first_given"]): # genus[i]
            i = self.envD["first_given"][6:-1]
            self.envD["first_given"] = genusL[i]
            self.envD["start_i"] = i+1

        if self.envD["ignorance_of_parentheses"]:
            for genus in genusL:
                for subgenus in genus.subgenusL:
                    subgenus.text = re.sub(r"\[ [^\[\]]* \] | \( [^()]* \)", "", subgenus.text, re.VERBOSE | re.DOTALL)

        if self.flag & SECOND_INNER_FAMILY != SECOND_INNER_FAMILY:
            print(self.familyL[i].name, end="\n\n\n")
            ...





        # family action type
        if len(self.typeL) == 1:
            if self.typeL[0] == "Sequence":
                print(self.envD["first_given"], end="")
                start_i = self.envD["start_i"]
                for i, genus in enumerate(genusL[start_i:], start=start_i):
                    if flag & MEMORIZING_SEQUENCE:
                        # First step: Memorizing while watching
                        answer_streak = 0
                        while answer_streak < 3:
                            print(genus)
                            answer_streak = answer_streak + 1 if check_answer(get_input(len(genus.subgenusL)), genus.subgenusL) else 0

                            print()

                        # Second step: Memorizing without watching
                        answer_streak = 0
                        while answer_streak < 3:
                            os.system("cls")
                            answer_streak = answer_streak + 1 if check_answer(get_input(len(genus.subgenusL)), genus.subgenusL) else 0

                            input("\nPRESS ANY KEY")
                            os.system("cls")

                        # Third step: Memorizing all at once
                        init("\n".join([_raw_family_types, _raw_env, self.name] + genusL[:i+1]))

                        os.system("cls")
                    else:
                        check_answer(get_input(len(genus.subgenusL)), genus.subgenusL)

                        print()

            elif self.typeL[0] == "List":
                for genus in genusL:
                    subgenusL = [subgenus.strip() for subgenus in genus.split("\n") if subgenus.strip()]
                    check_answer(get_input(len(subgenusL)), subgenusL)

                    print()

            elif self.typeL[0] == "Q&A":
                genusL = [[line.strip() for line in genus.strip().split("\n")]
                    for genus in genusL]


                # randomly select `chosen_genus` from `genusL`
                shuffle(genusL)
                print(self.envD["suggestion"], end="")
                for chosen_genus in genusL:
                    # random question
                    print(chosen_genus[0])

                    # check answer
                    check_answer(get_input(len(chosen_genus)-1), chosen_genus[1:])
                    print()

            elif self.typeL[0] == "Q&Q":
                genusL = [[[genus.strip().split("\n")[0].strip(),], [line.strip() for line in genus.strip().split("\n")[1:]]]
                    for genus in genusL]


                # randomly select `chosen_genus` from `genusL`
                shuffle(genusL)
                print(self.envD["suggestion"], end="")
                for chosen_genus in genusL:
                    # random question
                    shuffle(chosen_genus)
                    print("\n".join(chosen_genus[0]))

                    # check answer
                    check_answer(get_input(len(chosen_genus[1])), chosen_genus[1])
                    print()

            elif re.compile(r"(Q&)+Q").match(self.typeL[0]): # Q&Q&Q, Q&Q&Q&Q, ...
                n = self.typeL[0].count("Q") - 1

                genusL = [[line.strip() for line in genus.strip().split("\n")]
                    for genus in genusL]


                # randomly select `chosen_genus` from `genusL`
                shuffle(genusL)
                print(self.envD["suggestion"], end="")
                for chosen_genus in genusL:
                    # random question
                    shuffle(chosen_genus)
                    print(chosen_genus[0])

                    # check answer
                    check_answer(get_input(n), chosen_genus[1:])
                    print()

            elif self.typeL[0] == "Category":
                category_manager = Category_manager()
                for category in _maintext.split("\n\n"):
                    category_name, *raw_elementL = category.strip().split("\n")
                    elementL = [raw_element.strip() for raw_element in raw_elementL]
                    category_manager.add_category(category_name, elementL)

                genusL = category_manager.get_all_elements()
                shuffle(genusL)
                for chosen_genus in genusL:
                    print(chosen_genus)

                    check_answer(get_input(1), category_manager.get_category(chosen_genus))
                    print()

            elif self.typeL[0] == "2-way Category": # Category + Q&A
                ... #FIXME

            else:
                raise UnknownFamilyType(*self.typeL)



            print()



        elif len(self.typeL) == 2:
            if self.typeL[0] == "Selection":
                inner_family_type = f"_SELECTION, {self.typeL[1]}"
                init(f"<{inner_family_type}>\n" + f"\n\n\n\n<{inner_family_type}>\n".join(genusL), INNER_FAMILY)

            elif self.typeL[0] == "_SELECTION":
                genus = _maintext
                subgenusL = [subgenus for subgenus in genus.split("\n\n") if subgenus.strip()]
                shuffle(subgenusL)

                inner_family_type = self.typeL[1]
                init(f"<{inner_family_type}>\n{self.name}\n{subgenusL[0]}", SECOND_INNER_FAMILY)

            else:
                raise UnknownFamilyType(*self.typeL)

        else:
            raise UnknownFamilyType(*self.typeL)


class Phylum:
    def __init__(self, text: str, flag: int = 0):
        self.familyL: list[Family] = []
        self.flag = flag
        ...




answer_stack: list[bool] = []

@multimethod
def check_answer(given_answer: str, right_answer: str): #type: ignore
    if given_answer != right_answer:
        print(right_answer + "    --INCORRECT")
        answer_stack.append(False)
        return False
    else:
        answer_stack.append(True)
        return True

@multimethod
def check_answer(given_answerL: list, right_answer: str): #type: ignore
    if len(given_answerL) != 1:
        raise Exception("Answer size should be 1")

    if given_answerL[0] != right_answer:
        print(right_answer + "    --INCORRECT")
        answer_stack.append(False)
        return False
    else:
        answer_stack.append(True)
        return True

@multimethod
def check_answer(given_answerL: list, right_answerL: tuple): #type: ignore
    if all(given_answer in right_answerL for given_answer in given_answerL):
        answer_stack.append(True)
        return True
    else:
        given_answerI = (given_answer for given_answer in given_answerL)
        right_answerI = (right_answer for right_answer in right_answerL
            if right_answer not in given_answerL)

        for given_answer in given_answerI:
            if given_answer in right_answerL:
                print(given_answer + "    --CORRECT")
            else:
                print(next(right_answerI) + "    --INCORRECT") #FIXME: print properly matching right_answer based on given_answerd

        answer_stack.append(False)
        return False

@multimethod
def check_answer(given_answerL: list, right_answerL: list):
    if all(given_answer in right_answerL for given_answer in given_answerL):
        answer_stack.append(True)
        return True
    else:
        given_answerI = (given_answer for given_answer in given_answerL)
        right_answerI = (right_answer for right_answer in right_answerL
            if right_answer not in given_answerL)

        for given_answer in given_answerI:
            if given_answer in right_answerL:
                print(given_answer + "    --CORRECT")
            else:
                print(next(right_answerI) + "    --INCORRECT") #FIXME: print properly matching right_answer based on given_answerd

        answer_stack.append(False)
        return False

def get_input(n: int):
    _out: list[str] = []
    while len(_out) != n:
        _temp = input().strip()
        if _temp:
            _out.append(_temp)

    return _out





def get_txt(domain_name="", phylum_name=""):
    if not domain_name:
        domain_name = input("Domain Name: ")
    if not phylum_name:
        phylum_name = input("Phylum Name: ")

    with open(f"./data/{domain_name}/{phylum_name}.txt", "r", encoding="utf-8") as file:
        return "".join(file.readlines())



def init(text="", flag=0):
    global answer_stack
    
    if not text:
        text = get_txt()



    text = re.sub(r"/\*[^*]*\*+(?:[^/*][^*]*\*+)*/", "", text) # https://stackoverflow.com/questions/13014947/regex-to-match-a-c-style-multiline-comment


    # remove //
    text = re.sub(pattern=r"""
        // # //
        .* # (something in one line)
        """,

        repl="", string=text, flags=re.VERBOSE)

    text.replace("->", "→") #FIXME: family cannot include "<", ">"






    # divide text in familys
    familyL: list[str] = [family.strip()
        for family in re.compile(r"<[^<>]*>[^<>]*").findall(text) #FIXME: family cannot include "<", ">"
        if family.strip()]

    familyL = [family.replace("→", "->") for family in familyL] #FIXME: family cannot include "<", ">"



    # perform proper action for each family based on domain type
    shuffle(familyL)
    for family in familyL:
        if not (flag & INNER_FAMILY):
            os.system("cls")

        answer_stack = []







        if not (flag & INNER_FAMILY):
            print("\n")

            if all(answer_stack):
                print("Perfect!")

            input("End of the family.")
        else:
            print()


