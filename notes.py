from flask import session, request
from flask_restful import Resource
from models import Note, db

def get_current_user_id():
    """Helper to get authenticated user's ID from session."""
    return session.get('user_id')


class NoteList(Resource):
    def get(self):
        """GET /notes paginated list of current user's notes."""
        user_id = get_current_user_id()
        if not user_id:
            return {'error': 'Unauthorized'}, 401

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        paginated = Note.query.filter_by(user_id=user_id)\
                              .paginate(page=page, per_page=per_page, error_out=False)

        return {
            'notes': [note.to_dict() for note in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': paginated.page
        }, 200

    def post(self):
        """POST /notes create a new note."""
        user_id = get_current_user_id()
        if not user_id:
            return {'error': 'Unauthorized'}, 401

        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        if not title or not content:
            return {'error': 'Title and content are required'}, 422

        note = Note(title=title, content=content, user_id=user_id)
        db.session.add(note)
        db.session.commit()
        return note.to_dict(), 201


class NoteDetail(Resource):
    def get_note_or_403(self, note_id):
        """Fetch note and verify ownership. Returns (note, None) or (None, error_response)."""
        user_id = get_current_user_id()
        if not user_id:
            return None, ({'error': 'Unauthorized'}, 401)

        note = Note.query.get(note_id)
        if not note:
            return None, ({'error': 'Note not found'}, 404)

        if note.user_id != user_id:
            return None, ({'error': 'Forbidden'}, 403)

        return note, None

    def patch(self, note_id):
        """PATCH /notes/<id> update a note."""
        note, error = self.get_note_or_403(note_id)
        if error:
            return error

        data = request.get_json()
        if 'title' in data:
            note.title = data['title']
        if 'content' in data:
            note.content = data['content']

        db.session.commit()
        return note.to_dict(), 200

    def delete(self, note_id):
        """DELETE /notes/<id> delete a note."""
        note, error = self.get_note_or_403(note_id)
        if error:
            return error

        db.session.delete(note)
        db.session.commit()
        return {}, 204