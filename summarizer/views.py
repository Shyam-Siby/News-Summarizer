from datetime import date
import os
import tempfile
from PIL import Image  # Correct import

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from summarizer.models import Summary
from .algorithms.scoring import scoring_algorithm, scoring_nepali
from .algorithms.frequency import extraction, frequency_nepali, frequency_algorithm
from .algorithms.sentiment_analysis import analyze_sentiment
from .algorithms.visualization import plot_sentiment
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from .models import MyModel
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas  # Import canvas from reportlab
from django.http import HttpResponse
from io import BytesIO
import base64

import nltk
nltk.download('punkt')

def index(request):
    return render(request, 'summarizer/index.html')

def summarize_page(request):
    url = request.GET.get('url')
    long_text = request.GET.get('long-text')
    sentence_no = int(request.GET.get('number'))
    algorithm = request.GET.get('algorithm')
    result_list = []

    if url:
        long_text = extraction.extract(url)  # text extraction using BS
        original_text = url
    else:
        original_text = long_text

    if algorithm == '1':
        result_list = scoring_algorithm.scoring_main(long_text, sentence_no)
    elif algorithm == '2':
        result_list = frequency_algorithm.frequency_main(long_text, sentence_no)

    summary = ' '.join(result_list)
    sentiment = analyze_sentiment(summary)
    sentiment_plot = plot_sentiment(sentiment)

    context = {
        'data': summary,
        'original_text': original_text,
        'sentiment': sentiment,
        'sentiment_plot': sentiment_plot
    }
    return render(request, "summarizer/index.html", context)

def summarize_nepali_page(request):
    url = request.GET.get('url')
    long_text = request.GET.get('long-text')
    sentence_no = int(request.GET.get('number'))
    algorithm = request.GET.get('algorithm')
    result_list = []

    if url:
        long_text = extraction.extract(url)
        original_text = url
    else:
        original_text = long_text

    if algorithm == '1':
        result_list = scoring_nepali.scoring_main(long_text, sentence_no)
    elif algorithm == '2':
        result_list = frequency_nepali.frequency_main_nepali(long_text, sentence_no)

    summary = ' '.join(result_list)

    context = {'data': summary, 'original_text': original_text}
    return render(request, "summarizer/index.html", context)

@login_required
def save_summary(request):
    summary = request.POST.get('summary')
    topic = request.POST.get('topic')
    if len(topic) < 50:
        heading = topic
    else:
        heading = topic[:50] + '...'

    sentiment = analyze_sentiment(summary)
    sentiment_plot = plot_sentiment(sentiment)

    summaryTb = Summary(
        user=request.user,
        body=summary,
        original_link=heading,
        sentiment_classification=sentiment['classification'],
        sentiment_polarity=sentiment['polarity'],
        sentiment_subjectivity=sentiment['subjectivity'],
        sentiment_plot=sentiment_plot,
        date_created=date.today()
    )
    summaryTb.save()
    context = {'message': 'success'}
    return render(request, "summarizer/index.html", context)

def history(request):
    summary = Summary.objects.filter(user=request.user).order_by('-id')
    context = {'data': summary}
    return render(request, "summarizer/history.html", context)

def history_topic(request):
    if request.method == 'GET':
        topic = request.GET.get('topic')
        summary_body = request.GET.get('body')
        
        try:
            summaries = Summary.objects.filter(original_link=topic, body=summary_body)
            if summaries.exists():
                summary_obj = summaries.first()  # or handle multiple summaries as needed
                context = {
                    'topic': topic,
                    'body': summary_body,
                    'summary_id': summary_obj.id,
                    'sentiment_classification': summary_obj.sentiment_classification,
                    'sentiment_polarity': summary_obj.sentiment_polarity,
                    'sentiment_subjectivity': summary_obj.sentiment_subjectivity,
                    'sentiment_plot': summary_obj.sentiment_plot
                }
            else:
                context = {
                    'error': 'No matching summary found.'
                }
        except MultipleObjectsReturned:
            summaries = Summary.objects.filter(original_link=topic, body=summary_body)
            summary_obj = summaries.first()  # or handle multiple summaries as needed
            context = {
                'topic': topic,
                'body': summary_body,
                'summary_id': summary_obj.id,
                'sentiment_classification': summary_obj.sentiment_classification,
                'sentiment_polarity': summary_obj.sentiment_polarity,
                'sentiment_subjectivity': summary_obj.sentiment_subjectivity,
                'sentiment_plot': summary_obj.sentiment_plot
            }
        except ObjectDoesNotExist:
            context = {
                'error': 'No matching summary found.'
            }
    else:
        context = {
            'error': 'Invalid request method.'
        }
    return render(request, "summarizer/history_topic.html", context)

def download_summary_pdf(request, summary_id):
    # Fetch the summary from the database
    summary = get_object_or_404(Summary, id=summary_id)

    # Create a PDF buffer
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Margins and line spacing
    margin_x = 30
    margin_y = 30
    line_spacing = 14  # Space between lines
    content_width = width - 2 * margin_x  # Content width considering margins

    # Add title for the summary section
    text = p.beginText(margin_x, height - margin_y)
    text.setFont("Helvetica-Bold", 14)
    text.textLine("Summary")

    # Add structured summary text (tokenize into sentences)
    summary_sentences = nltk.sent_tokenize(summary.body)
    text.setFont("Helvetica", 12)
    
    # Handle pagination
    current_height = height - margin_y - 20  # Leave space for the header
    for sentence in summary_sentences:
        sentence_height = text.getY() - line_spacing
        if sentence_height < margin_y:  # If the text goes below the margin
            p.drawText(text)
            p.showPage()
            text = p.beginText(margin_x, height - margin_y)
            text.setFont("Helvetica", 12)
        text.textLine(sentence)

    # Add space after the summary
    text.moveCursor(0, line_spacing)
    
    # Draw the text
    p.drawText(text)

    # Start a new page for sentiment analysis if necessary
    if text.getY() < margin_y:
        p.showPage()
        text = p.beginText(margin_x, height - margin_y)
    
    # Add sentiment analysis details
    text.setFont("Helvetica-Bold", 14)
    text.textLine("Sentiment Analysis")

    text.setFont("Helvetica", 12)
    text.textLines(f"Polarity: {summary.sentiment_polarity}\n")
    text.textLines(f"Subjectivity: {summary.sentiment_subjectivity}\n")

    # Draw the text
    p.drawText(text)

    # Handle the image
    plot_data = base64.b64decode(summary.sentiment_plot)
    plot_buffer = BytesIO(plot_data)

    # Save plot_buffer to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        temp_file.write(plot_buffer.getvalue())
        temp_file_path = temp_file.name

    # Use PIL to open and resize the image to fit properly
    with Image.open(temp_file_path) as img:
        img_width, img_height = img.size
        
        # Adjust image size to fit within PDF content width while keeping the aspect ratio
        max_img_width = content_width
        aspect_ratio = img_height / img_width
        adjusted_img_height = max_img_width * aspect_ratio

        # Make sure the image doesn't exceed a certain height
        if adjusted_img_height > 200:  # Max height limit
            adjusted_img_height = 200
            max_img_width = adjusted_img_height / aspect_ratio
        
        # Draw the image on a new page if there's not enough space
        if text.getY() < adjusted_img_height + margin_y:
            p.showPage()
        p.drawImage(temp_file_path, margin_x, text.getY() - adjusted_img_height, width=max_img_width, height=adjusted_img_height)

    # Finalize the PDF
    p.showPage()
    p.save()

    # Prepare the response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=summary_{summary_id}.pdf'

    return response

def my_view(request, pk):
    # Retrieve the object or return a 404 error if not found
    my_object = get_object_or_404(MyModel, pk=pk)
    
    # Render the template with the context
    return render(request, 'summarizer/my_template.html', {'object': my_object})
