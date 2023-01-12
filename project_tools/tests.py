from unittest import TestCase

from project_tools.classes import GuitarNotes

class NotesClassTest(TestCase):

    def test_valid_root_note(self):
        new_object = GuitarNotes()
        note = 'A'
        self.assertEqual(note, new_object.set_root_note(note))
        second_note = 'F#'
        self.assertEqual(second_note, new_object.set_root_note(second_note))

    def test_valid_lower_case_note(self):
        new_object = GuitarNotes()
        lower_case_note = 'd#'
        self.assertEqual('D#', new_object.set_root_note(lower_case_note))

    def test_invalid_root_note_raise_error(self):
        new_object = GuitarNotes()
        wrong_note = ''
        with self.assertRaises(ValueError):
            new_object.set_root_note(wrong_note)

    def test_valid_minor_chord(self):
        new_object = GuitarNotes()
        scale = new_object.show_the_scale('f', 'major')
        self.assertEqual(scale, ['F', 'A', 'C'])

    def test_invalid_chord(self):
        new_object = GuitarNotes()
        with self.assertRaises(ValueError):
            new_object.show_the_scale('', '')
        with self.assertRaises(KeyError):
            new_object.show_the_scale('b', 'mjor')
