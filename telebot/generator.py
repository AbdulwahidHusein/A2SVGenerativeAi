import sys

sys.path.append("..")
from api import api_caller_v2
from file_processor import file_reader, file_summerizer, file_chunk, keyword_extractor


def read_summerize_split(file, start_page, end_page):
    """read and summerise"""
    reader = file_reader.FileReader(file)
    if end_page - start_page > 10:
        end_page = start_page + 10

    file_content = reader.read_file(start_page, end_page)
    splitted = []
    divider = 2
    if file_content:
        summerizer = file_summerizer.Summerizer(file_content)
        summerized = summerizer.summarize(
            divider
        )  # 1/3 of the original number of sentence
        splitted = file_chunk.split_text_into_groups(summerized, 100, 500)

        while len(splitted) > 5:
            summerizer = file_summerizer.Summerizer(" ".join(splitted))
            summerized = summerizer.summarize(
                divider
            )  # 1/3 of the original number of sentence
            splitted = file_chunk.split_text_into_groups(summerized, 100, 500)

        return splitted
    else:
        # this should be error
        return ["file not found"]

    """make a prompt"""


# another alternative
def red_extract_keyword(file, start_page, end_page):
    end_page = min(start_page + 30, end_page)
    reader = file_reader.FileReader(file)
    file_content = reader.read_file(start_page, end_page)

    keywwords = keyword_extractor.extract_keywords(
        file_content, (end_page - start_page) * 10
    )
    return keywwords
    raise Exception("error reading a file")


def get_question(file, num_of_questions, difficulty, start_page, end_page, mode, model):
    num_of_questions = max(int(num_of_questions), num_of_questions)
    # mode can be multiple_choice or short_answer
    # summerized_data = read_summerize_split(file, start_page, end_page)
    keywords = red_extract_keyword(
        file, start_page, end_page
    )  # for now we use kewords instead
    summerized_data = keywords
    if summerized_data:
        # print(summerized_data)
        # use v2
        question_generator = api_caller_v2.GenerateQuestionRequest(
            summerized_data, model
        )
        questions = question_generator.make_request(num_of_questions, difficulty, mode)

        return questions
    else:
        # this should be handled in views.py
        return False


def get_q():
    return {
        "questions": [
            {
                "question": "How does the relative atomic mass of an element compare to its atomic mass?",
                "optionA": "The relative atomic mass is greater than the atomic mass",
                "optionB": "The relative atomic mass is equalto the atomic mass",
                "optionC": "The relative atomic mass is less than the atomic mass",
                "optionD": "It dependson the element",
                "correctOption": "optionB",
                "explanation": " The relative atomic mass of an element is the same as its atomic mass, since it is the average mass of the element s atoms. ",
            },
            {
                "question": "What does the principal quantum number (n) represent?",
                "optionA": "The number of protons in an atom",
                "optionB": "The number of electrons in an atom",
                "optionC": "The energy of an electron",
                "optionD": "The size of an orbital",
                "correctOption": "optionD",
                "explanation": " The principal quantum number (n) represents the size of an orbital, which is determined by the energy level of the electron. It is also used to describe the location of an electron within an atom. ",
            },
            {
                "question": "What is the Pauli Exclusion Principle?",
                "optionA": "It states that electrons must occupy different orbitals",
                "optionB": "It states that two electrons cannot have the same set of quantum numbers",
                "optionC": "It states that two electrons can occupy the same orbital",
                "optionD": "It states that electrons must occupy the same orbital",
                "correctOption": "optionB",
                "explanation": " The Pauli Exclusion Principle states that two electrons cannot have the same set of quantum numbers, meaning that they must occupy different orbitals. This principle is important in understanding the behavior of electrons in atoms. ",
            },
            {
                "question": "What is the maximum number of electrons that can occupy a single orbital?",
                "optionA": "One",
                "optionB": "Two",
                "optionC": "Three",
                "optionD": "Four",
                "correctOption": "optionA",
                "explanation": " According to the Pauli Exclusion Principle, the maximum number of electrons that can occupy a single orbital is one. This means that two electrons cannot occupy the same orbital. ",
            },
            {
                "question": "What is the relative formula mass of a compound?",
                "optionA": "The sum ofthe atomic masses of the elements in the compound",
                "optionB": "The sum of the relative atomic masses of the elements in the compound",
                "optionC": "The sum of the nuclear charges of the elements in the compound",
                "optionD": "The sum of the ionization energies of the elements in the compound",
                "correctOption": "optionB",
                "explanation": " The relative formula mass of a compound is the sum of the relative atomic masses of the elements in the compound. This is also known as the molecular mass or molar mass. ",
            },
            {
                "question": "What does the periodic table of elements show?",
                "optionA": "The symbols of elements",
                "optionB": "The number of electrons in an atom",
                "optionC": "The atomic masses of elements",
                "optionD": "The properties of elements",
                "correctOption": "optionD",
                "explanation": " The periodic table of elements shows the properties of different elements, such as their symbols, atomic masses, and number of electrons. It is used to organize and compare elements based on their chemical and physical properties. ",
            },
            {
                "question": "What is the atomic radius of an element?",
                "optionA": "The distance between the nucleus and the outermost electron",
                "optionB": "The distance between the nucleus and the innermost electron",
                "optionC": "The distance between the nucleus and the center of the atom",
                "optionD": "The distance between thenucleus and the center of the orbital",
                "correctOption": "optionA",
                "explanation": " The atomic radius of an element is the distance between the nucleus and the outermost electron. This is an important property of atoms, asit helps to determine the size, shape, and reactivity of the atom. ",
            },
            {
                "question": "What is the relationship between the atomic number and the number of electrons in an atom?",
                "optionA": "The atomic number is equal to thenumber of electrons",
                "optionB": "The atomic number is greater than the number of electrons",
                "optionC": "The atomic number is less than the number of electrons",
                "optionD": "The atomic number has no relation to the number of electrons",
                "correctOption": "optionA",
                "explanation": " The atomic number of an atom is equal to the number of electrons in the atom. This is because the number of protons in the nucleus of an atom is equal to the numberof electrons in the atom. ",
            },
            {
                "question": "What is the difference between relative atomic mass and relative molecular mass?",
                "optionA": "The relative atomic mass is the average mass of an atom, while the relative molecular mass is the average mass of a molecule",
                "optionB": "The relative atomic mass is the total mass of an atom, while the relative molecular mass is the total mass of a molecule",
                "optionC": "The relative atomic mass is the average mass of a molecule, while the relative molecular mass is the average mass of an atom",
                "optionD": "The relative atomic mass is the total mass of a molecule, while the relative molecular mass is the total mass of an atom",
                "correctOption": "optionA",
                "explanation": " The relative atomic mass is the average mass of an atom, while the relative molecular mass is the average mass of a molecule. This is because atoms are the smallest particles that make up a molecule, and the average mass of a molecule is made up of the average mass of its constituent atoms. ",
            },
            {
                "question": "What is the electron configuration of a gaseous atom?",
                "optionA": "The arrangement of electrons in the orbitals of the atom",
                "optionB": "The arrangement of protons in the nucleus of the atom",
                "optionC": "The arrangement of neutrons in the nucleus of the atom",
                "optionD": "The arrangement of electrons in the nucleus of the atom",
                "correctOption": "optionA",
                "explanation": " The electron configuration of a gaseous atom is the arrangement of electrons in the orbitals of the atom. This is important in understanding the chemical properties of the atom, as it determines how it will interact with other atoms and molecules.",
            },
        ]
    }


if __name__ == "__main__":
    with open(
        "c:\\Users\\Abdi\\Desktop\\A2SVGenerativeAi\\quiz_app/drf.pdf", "rb"
    ) as df:
        q = get_question(df, 5, "hard", 30, 50, "multiple_choice", "chatgpt")
        print(q)
        """f = read_summerize_split(df, 10,  100)
        print(f)
        print('\n\n\n\n\n\n')
        print(len(f))"""
