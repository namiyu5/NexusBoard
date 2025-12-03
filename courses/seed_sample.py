from courses.models import Course, Lesson

def seed():
    samples = [
        {
            'title': 'Intro to Web Development',
            'excerpt': 'Learn HTML, CSS, and JavaScript basics.',
            'published': True,
            'lessons': [
                ('HTML Basics', 'Tags, structure, semantic HTML.'),
                ('CSS Fundamentals', 'Selectors, box model, layout.'),
                ('Intro to JavaScript', 'Variables, DOM, events.'),
            ]
        },
        {
            'title': 'Python for Beginners',
            'excerpt': 'Start coding with Python and build simple apps.',
            'published': True,
            'lessons': [
                ('Python Syntax', 'Variables, types, control flow.'),
                ('Functions & Modules', 'Organizing code into functions and modules.'),
            ]
        }
    ]

    for s in samples:
        course, created = Course.objects.get_or_create(
            title=s['title'],
            defaults={'excerpt': s['excerpt'], 'published': s['published']}
        )
        if created:
            print('Created course:', course.title)
        else:
            print('Found course:', course.title)

        for idx, (ltitle, lcontent) in enumerate(s['lessons'], start=1):
            lesson, lcreated = Lesson.objects.get_or_create(
                course=course, title=ltitle,
                defaults={'content': lcontent, 'order': idx}
            )
            if lcreated:
                print('  Created lesson:', lesson.title)
            else:
                print('  Found lesson:', lesson.title)

if __name__ == '__main__':
    seed()
