import re
from random import shuffle, getrandbits
import os
from multimethod import multimethod



INNER_FAMILY = 0b1
SECOND_INNER_FAMILY = 0b11
MANUAL_GENUS_SEPARATOR = 0b100
MEMORIZING_SEQUENCE = 0b1000
REPEAT_COUNT = 3

SPECIAL_FAMILY_TYPE = ("Selection", "_SELECTION")
INDENT = "    "




# data structure

# data (folder)
# └ domain1 (folder)
#   └ phylum1 (.txt file)
#     └ family1
#       ├ genus1
#       ├ genus2
#       │ └ subgenus2.1
#       └ genus3







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

        _raw_family_types = family.split("\n")[0]
        family_typeL = _raw_family_types[1:-1].split(", ")
        family_typeL.sort(key=lambda _type: _type not in SPECIAL_FAMILY_TYPE)
        family_attributeD = {
            "genus_separator": "\n",
            "first_given": "",
            "start_i": 0,
            "ignorance_of_parentheses": False,
            "suggestion": "",
            "indented_multiline_genus": False,
        }


        is_manual_genus_separator: bool = False
        if re.compile(r"\[.*\]").match(family.split("\n")[1]):
            _raw_family_attribute = family.split("\n")[1]
            _key_value_pairL = _raw_family_attribute[1:-1].split(", ")

            family_name = family.split("\n")[2]
            family_maintext = "\n".join(family.split("\n")[3:])
        else:
            _raw_family_attribute = ''
            _key_value_pairL = []
            
            family_name = family.split("\n")[1]
            family_maintext = "\n".join(family.split("\n")[2:])

        _appending_family_attributeD = dict(_key_value_pair.split(": ") for _key_value_pair in _key_value_pairL)
        _appending_family_attributeD = \
            {key:
                re.compile(r"\\n").sub("\n", value[1:-1])   if re.compile(r""" ".*" | '.*' """, re.VERBOSE).match(value)
                else int(value) if value.isnumeric()
                else True if value in ("True", "true")
                else False if value in ("False", "false")
                else value
            for key, value in _appending_family_attributeD.items()
            }

        family_attributeD.update(_appending_family_attributeD)
        
        if "genus_separator" in _appending_family_attributeD.keys():
            is_manual_genus_separator = True




        min_genus_separatorD = {
            "List": "\n\n",
            "Q&A": "\n\n",
            "Q&Q": "\n\n",
            "Q&Q&Q": "\n\n", #FIXME: Q&Q&Q&Q...
            "Selection": "\n\n\n",
        }




        if not is_manual_genus_separator:
            for family_type in family_typeL:
                if (genus_separator:=min_genus_separatorD.get(family_type)) and family_attributeD["genus_separator"] == "\n":
                    family_attributeD["genus_separator"] = genus_separator


        if family_attributeD["indented_multiline_genus"] and not flag & MEMORIZING_SEQUENCE:
            pre_genusL = family_maintext.split(family_attributeD["genus_separator"])
            genusL = [""]*len(pre_genusL)
            i = 0
            for pre_genus in pre_genusL:
                if pre_genus.strip():
                    if re.match(rf"^{INDENT*2}", pre_genus): #FIXME: the condition have to be relative to other lines; not absolute `INDENT*2`
                        i -= 1
                        genusL[i] += " " + pre_genus.strip()
                    else:
                        genusL[i] += pre_genus.strip()


                    i += 1

            # remove all `""` in `genusL`
            try:
                while True:
                    genusL.remove("")
            except:
                pass
        else:
            genusL = [pre_genus.strip() for pre_genus in family_maintext.split(family_attributeD["genus_separator"]) if pre_genus.strip()]

        if re.match(r"^genus\[\d+\]$", family_attributeD["first_given"]): # genus[i]
            i = family_attributeD["first_given"][6:-1]
            family_attributeD["first_given"] = genusL[i]
            family_attributeD["start_i"] = i+1

        if family_attributeD["ignorance_of_parentheses"]:
            pattern = re.compile(r"""
                  \[ [^\[\]]* \]   #    Packed by square brackets
                | \( [^()]* \)     # Or Packed by parentheses
            """, re.VERBOSE)
            genusL = [pattern.sub("", genus) for genus in genusL]






        if flag & SECOND_INNER_FAMILY != SECOND_INNER_FAMILY:
            print(family_name, end="\n\n\n")






        # family action type
        if len(family_typeL) == 1:
            if family_typeL[0] == "Sequence":
                print(family_attributeD["first_given"], end="")
                start_i = family_attributeD["start_i"]
                for i, genus in enumerate(genusL[start_i:], start=start_i):
                    subgenusL = [subgenus.strip() for subgenus in genus.split("\n") if subgenus.strip()]
                    if flag & MEMORIZING_SEQUENCE:
                        # First step: Memorizing while watching
                        answer_streak = 0
                        while answer_streak < REPEAT_COUNT:
                            print(genus)
                            answer_streak = answer_streak + 1 if check_answer(get_input(len(subgenusL)), subgenusL) else 0

                            print()

                        # Second step: Memorizing without watching
                        answer_streak = 0
                        while answer_streak < REPEAT_COUNT:
                            os.system("cls")
                            answer_streak = answer_streak + 1 if check_answer(get_input(len(subgenusL)), subgenusL) else 0

                            input("\nPRESS ANY KEY")
                            os.system("cls")

                        # Third step: Memorizing all at once
                        if _raw_family_attribute:
                            init("\n".join([_raw_family_types, _raw_family_attribute, family_name] + genusL[:i+1]))
                        else:
                            init("\n".join([_raw_family_types, family_name] + genusL[:i+1]))

                        os.system("cls")
                    else:
                        check_answer(get_input(len(subgenusL)), subgenusL)

                        print()

            elif family_typeL[0] == "List":
                for genus in genusL:
                    subgenusL = [subgenus.strip() for subgenus in genus.split("\n") if subgenus.strip()]
                    check_answer(get_input(len(subgenusL)), subgenusL)

                    print()

            elif family_typeL[0] == "Q&A":
                genusL = [[line.strip() for line in genus.strip().split("\n")]
                    for genus in genusL]


                # randomly select `chosen_genus` from `genusL`
                shuffle(genusL)
                print(family_attributeD["suggestion"], end="")
                for chosen_genus in genusL:
                    # random question
                    print(chosen_genus[0])

                    # check answer
                    check_answer(get_input(len(chosen_genus)-1), chosen_genus[1:])
                    print()

            elif family_typeL[0] == "Q&Q":
                genusL = [[[genus.strip().split("\n")[0].strip(),], [line.strip() for line in genus.strip().split("\n")[1:]]]
                    for genus in genusL]


                # randomly select `chosen_genus` from `genusL`
                shuffle(genusL)
                print(family_attributeD["suggestion"], end="")
                for chosen_genus in genusL:
                    # random question
                    shuffle(chosen_genus)
                    print("\n".join(chosen_genus[0]))

                    # check answer
                    check_answer(get_input(len(chosen_genus[1])), chosen_genus[1])
                    print()

            elif re.compile(r"(Q&)+Q").match(family_typeL[0]): # Q&Q&Q, Q&Q&Q&Q, ...
                n = family_typeL[0].count("Q") - 1

                genusL = [[line.strip() for line in genus.strip().split("\n")]
                    for genus in genusL]


                # randomly select `chosen_genus` from `genusL`
                shuffle(genusL)
                print(family_attributeD["suggestion"], end="")
                for chosen_genus in genusL:
                    # random question
                    shuffle(chosen_genus)
                    print(chosen_genus[0])

                    # check answer
                    check_answer(get_input(n), chosen_genus[1:])
                    print()

            elif family_typeL[0] == "Category":
                category_manager = Category_manager()
                for category in family_maintext.split("\n\n"):
                    category_name, *raw_elementL = category.strip().split("\n")
                    elementL = [raw_element.strip() for raw_element in raw_elementL]
                    category_manager.add_category(category_name, elementL)

                genusL = category_manager.get_all_elements()
                shuffle(genusL)
                for chosen_genus in genusL:
                    print(chosen_genus)

                    check_answer(get_input(1), category_manager.get_category(chosen_genus))
                    print()

            elif family_typeL[0] == "2-way Category": # Category + Q&A
                ... #FIXME

            else:
                raise UnknownFamilyType(*family_typeL)



            print()



        elif len(family_typeL) == 2:
            if family_typeL[0] == "Selection":
                inner_family_type = f"_SELECTION, {family_typeL[1]}"
                init(f"<{inner_family_type}>\n" + f"\n\n\n\n<{inner_family_type}>\n".join(genusL), INNER_FAMILY)

            elif family_typeL[0] == "_SELECTION":
                genus = family_maintext
                subgenusL = [subgenus for subgenus in genus.split("\n\n") if subgenus.strip()]
                shuffle(subgenusL)

                inner_family_type = family_typeL[1]
                init(f"<{inner_family_type}>\n{family_name}\n{subgenusL[0]}", SECOND_INNER_FAMILY)

            else:
                raise UnknownFamilyType(*family_typeL)

        else:
            raise UnknownFamilyType(*family_typeL)


        if not (flag & INNER_FAMILY):
            print("\n")

            if all(answer_stack):
                print("Perfect!")

            input("End of the family.")
        else:
            print()


