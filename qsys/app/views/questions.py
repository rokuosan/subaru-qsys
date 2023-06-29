import datetime
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from app.models.category import CtfQuestionCategory
from app.models.ctf_information import CtfInformation
from app.models.difficulty import CtfQuestionDifficulty
from app.models.history import CtfAnswerHistory
from app.models.question import CtfQuestion
from app.models.score import CtfScore


@login_required
def questions(request: HttpRequest):
    """問題一覧を表示するView"""
    ctx = {
        # 'list': [{
        #     'category': 'category_name',
        #     'questions': [],
        # }]
        'list': []
    }

    # Questionから全データを取得して、辞書型に変換
    questions = CtfQuestion.objects.all().values()
    categories = CtfQuestionCategory.objects.all().values()
    diffs = CtfQuestionDifficulty.objects.all().values()

    # カテゴリ名を持った辞書を作成し、ctx['list']に追加
    for c in categories:
        info = {}
        info['category'] = c['category_name']
        ctx['list'].append(info)

    # 問題データに難易度名を追加し、カテゴリが対応するctx['list']に追加
    for q in questions:
        cn = categories.get(pk=q['category_id'])['category_name']
        dn = diffs.get(difficulty_id=q['difficulty_id'])['name']

        for li in ctx['list']:
            if li['category'] == cn:
                if 'questions' not in li.keys():
                    li['questions'] = []

                q['difficulty_name'] = dn
                li['questions'].append(q)
                break

    # カテゴリ名をcapitalize
    for li in ctx['list']:
        li['category'] = li['category'].replace('_', ' ').capitalize()

    return render(request, 'app/questions.html', ctx)


def question_detail(request: HttpRequest, question_id: int):
    """問題の詳細を表示するView"""
    ctx = {}
    question = get_object_or_404(CtfQuestion, pk=question_id)
    ctx['question'] = question
    ctx['status'] = 'in_progress'

    # POST /questions/<int:question_id>/
    if request.method == 'POST':
        # Get sent answer
        answer = request.POST.get('answer')

        if (answer == None or answer == ''):
            ctx['status'] = 'invalid'
            return render(request, 'app/questions/content.html', ctx)

        print(question)
        # Check answer
        is_correct = question.flag == answer
        if is_correct:
            # 正解を表示
            ctx['status'] = 'correct'

            # 開催中のCTFを取得
            now = datetime.datetime.now()
            ctf = CtfInformation.objects.filter(
                start_at__lte=now, end_at__gte=now).first()

            # 回答済みかどうかを確認
            if CtfScore.objects.filter(user=request.user, ctf=ctf, question=question).exists():
                ctx['status'] = 'already_answered'
                return render(request, 'app/questions/content.html', ctx)

            # スコアを保存
            CtfScore.objects.create(
                user=request.user,
                ctf=ctf,
                question=question,
                point=question.point
            )

        else:
            # 不正解を表示
            ctx['status'] = 'incorrect'

        # 回答履歴を保存
        CtfAnswerHistory.objects.create(
            user=request.user,
            question=question,
            answered_content=answer,
            is_correct=is_correct
        )

    return render(request, 'app/questions/content.html', ctx)
