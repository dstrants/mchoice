import os
from docx2python import docx2python as converter
from docx2python.iterators import enum_cells, enum_at_depth
from .models import Test, Question, Choice


def locate_docxs():
    files = []
    for file in os.listdir('media/sources'):
        if file.endswith('.docx'):
            files.append(file)
    return files


def import_docxs(files):
    cnt = 0
    if not isinstance(files, list):
        files = [files]
    for file in files:
        try:
            tables = converter(file, html=True)
        except Exception as e:
            print(e)
        else:
            cnt += import_questions(tables.body, file)
    print("%s Questions Imported" % cnt)
    return True


def remove_empty_paragraphs(tables):
    for (i, j, k), cell in enum_cells(tables):
        tables[i][j][k] = [x for x in cell if x]
    return tables


def import_questions(tables, file):
    tables = remove_empty_paragraphs(tables)
    test, created = Test.objects.get_or_create(title=file)
    qcount = Question.objects.count()
    for (i, j, k, l), paragraph in enum_at_depth(tables, 4):
        if l % 6 == 0:
            q = Question.objects.create(title=paragraph, test=test)
        elif '<b>' in paragraph and l % 6 != 0:
            Choice.objects.create(title=paragraph, question=q,
                                  correct=True)
        elif l % 6 != 0:
            Choice.objects.create(title=paragraph, question=q)
        else:
            print(paragraph)
    return Question.objects.count() - qcount
