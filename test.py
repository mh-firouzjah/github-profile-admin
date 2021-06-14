def youtube(info):
    base = '<table>'
    for i, data in enumerate(info):
        title, link, published, thumbnail = data
        new_cel = f'<td><p align="center"><a href="{link}"><img alt="Forwarding" src="{thumbnail}" width="100%"><br><em overflow-wrap="break-word" style="color: grey">{title}</em></a></p></td>'
        if not i % 3:
            base += '<tr>'
        base += new_cel
        if not i % 3 or i == len(info) - 1:
            base += '</tr>'
    base += '</table>'
    return base
