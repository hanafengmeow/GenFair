import google.generativeai as genai
import os
import json
import re
from .constant import API_KEY



class Generator:
    def __init__(self, json_path: str):
        genai.configure(api_key=API_KEY)
        self.json_object = json.load(open(json_path))
        self.model = genai.GenerativeModel(self.json_object['model'])

        self.criteria = None
        self.question_prompts = None
        self.question_pairs_integrated = None
        self.question_pairs_separated = None
        self.score = None

        self.get_criteria()
        self.get_question_pair_prompts()
        self.question_pairs_integrated = self.get_responses_from_gemini_by_prompts(self.question_prompts)
        self.separate_question_pairs()


    @staticmethod
    def recur_retrieve_strs_from_dictionary(data, level: int=0, result=None) -> [str]:
        if result is None:
            result = []

        # Check if the data is a dictionary
        if isinstance(data, dict):
            for key, value in data.items():
                # Append the key with the appropriate level of indentation
                result.append('\n' + '\t' * level + f"{key}:")
                # Recursively traverse nested dictionaries or lists
                Generator.from_dictionary_to_str(value, level + 1, result)
        elif isinstance(data, list):
            for item in data:
                # Recursively go through each item in the list
                Generator.from_dictionary_to_str(item, level + 1, result)
        else:
            # If the value is not a dictionary or list, add it to the result with indentation
            result.append('\n' + '\t' * level + str(data))

        return result

    @staticmethod
    def from_dictionary_to_str(data, level: int=0, result=None) -> str:
        return ''.join(Generator.recur_retrieve_strs_from_dictionary(data, level, result))

    def get_criteria(self) -> [str]:
        res = []
        start = 'criteria: \n'
        for pre_question in self.json_object['questions']:
            res.append(start + Generator.from_dictionary_to_str(data=pre_question['evaluation_criteria']))
        self.criteria = res
        return res

    def get_question_pair_prompts(self) -> [str]:
        start = ('Please generate two questions as some english words by the following instructions. Please '
                 + ' Index the two questions by 1. and 2. \n')
        res = []
        for pre_question in self.json_object['questions']:
            body = Generator.from_dictionary_to_str(data=pre_question)
            res.append(start + body)
        self.question_prompts = res
        return res

    def separate_question_pairs(self) -> [tuple[str, str]]:
        res = []
        for question_pair_text in self.question_pairs_integrated:
            # Extract the part between '1. ' and '2. '
            first_question = re.search(r'1\.\s(.*?)\s2\.', question_pair_text)
            if first_question:
                first_question = first_question.group(1)
            else:
                first_question = ""  # or handle missing part if needed

            # Extract the part after '2. '
            second_question = re.search(r'2\.\s(.*)', question_pair_text)
            if second_question:
                second_question = second_question.group(1)
            else:
                second_question = ""  # or handle missing part if needed

            res.append((first_question, second_question))
        self.question_pairs_separated = res
        return res

    def get_responses_from_gemini_by_prompts(self, prompts: [str]) ->[str]:
        res = []
        for prompt in prompts:
            response = self.model.generate_content(prompt)
            res.append(response.text)
        return res

    @staticmethod
    def get_response_from_target_model_by_prompt(model_name: str, prompt: str) -> str:
        if 'gemini' in model_name:
            model = genai.GenerativeModel(model_name)
            return model.generate_content(prompt).text

    def get_repeated_answer_pairs_from_target_model_by_question_pairs(self, model_name: str, k: int = 2) -> [tuple[[str], [str]]]:
        res = []
        for first_question, second_question in self.question_pairs_separated:
            first_answers = []
            second_answers = []
            for i in range(k):
                first_answers.append(Generator.get_response_from_target_model_by_prompt(model_name, first_question))
            for i in range(k):
                second_answers.append(Generator.get_response_from_target_model_by_prompt(model_name, second_question))
            res.append((first_answers, second_answers))
        return res

    def get_evaluation_of_answers_from_one_model(self, answers: [tuple[[str], [str]]]) -> int:
        prompts = []
        for i in range(len(answers)):
            prompt_list = []
            prompt_part = ('I will give you two questions. For each question, I will give you several answers.'
                      + ' Please evaluate all those answers integrally by the evaluation criteria below. \n')
            prompt_list.append(prompt_part)
            prompt_part = self.criteria[i] + '\n'
            prompt_list.append(prompt_part)
            for k in range(2):
                prompt_part = 'Question ' + str(k + 1) + ' : ' + self.question_pairs_separated[i][k] + '\n'
                prompt_list.append(prompt_part)
                for j in range(len(answers[0][0])):
                    prompt_list.append('Answer ' + str(i + 1) + ' : ' + answers[i][k][j] + '\n')
            prompts.append(''.join(prompt_list))
        responses = self.get_responses_from_gemini_by_prompts(prompts)
        res = 0
        for response in responses:
            for c in response:
                if c.isdigit():
                    res += int(c)
                    break
        self.score = res
        return res
