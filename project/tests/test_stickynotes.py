import unittest
import json

from project.server import db
from project.server.models import StickyNote, User
from project.tests.base import BaseTestCase


class TestStickynoteBlueprint(BaseTestCase):
    def register_user(self, email, password):
        return self.client.post(
            "/auth/register",
            data=json.dumps(dict(
                email=email,
                password=password
            )),
            content_type="application/json"
        )

    def add_stickynote(self, note_content, user_id, register_response):
        return self.client.post(
            "/stickynote/add",
            data=json.dumps(dict(
                note_content=note_content,
                user_id=user_id
            )),
            headers=dict(
                Authorization="Bearer " + json.loads(
                    register_response.data.decode()
                )["auth_token"]
            ),
            content_type="application/json"
        )

    def test_add_sticky_note(self):
        register_response = self.register_user("jan@gmail.com", "test")
        user = User.query.filter_by(email="jan@gmail.com").first()
        response = self.add_stickynote("test", user.id, register_response)

        data = json.loads(response.data.decode())
        print(data)
        self.assertTrue(data["status"] == "success")
        self.assertTrue(data["message"] == "Successfully added.")
        self.assertTrue(response.content_type == "application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete_sticky_note(self):
        register_response = self.register_user("jan@gmail.com", "test")
        user = User.query.filter_by(email="jan@gmail.com").first()
        add_response = self.add_stickynote("test", user.id, register_response)
        sticky_note = StickyNote.query.filter_by(note_content="test").first()
        response = self.client.post(
            "/stickynote/delete",
            data=json.dumps(dict(
                id=sticky_note.id
            )),
            headers=dict(
                Authorization="Bearer " + json.loads(
                    register_response.data.decode()
                )["auth_token"]
            ),
            content_type="application/json"
        )

        data = json.loads(response.data.decode())
        print(data)
        self.assertTrue(data["status"] == "success")
        self.assertTrue(data["message"] == "Successfully deleted.")
        self.assertTrue(response.content_type == "application/json")
        self.assertEqual(response.status_code, 200)

    def test_update_sticky_note(self):
        register_response = self.register_user("jan@gmail.com", "test")
        user = User.query.filter_by(email="jan@gmail.com").first()
        add_response = self.add_stickynote("test", user.id, register_response)
        sticky_note = StickyNote.query.filter_by(note_content="test").first()
        response = self.client.post(
            "/stickynote/update",
            data=json.dumps(dict(
                id=sticky_note.id,
                note_content="new note content"
            )),
            headers=dict(
                Authorization="Bearer " + json.loads(
                    register_response.data.decode()
                )["auth_token"]
            ),
            content_type="application/json"
        )

        data = json.loads(response.data.decode())
        print(data)
        self.assertTrue(data["status"] == "success")
        self.assertTrue(data["message"] == "Successfully updated.")
        self.assertTrue(response.content_type == "application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_sticky_notes(self):
        register_response = self.register_user("jan@gmail.com", "test")
        user = User.query.filter_by(email="jan@gmail.com").first()
        self.add_stickynote("test", user.id)
        self.add_stickynote("test 1", user.id)
        self.add_stickynote("test 2", user.id)
        self.add_stickynote("test 3", user.id)

        response = self.client.get(
            "/stickynote/get?user_id=" + user.id,
            headers=dict(
                Authorization="Bearer " + json.loads(
                    register_response.data.decode()
                )["auth_token"]
            )
        )
