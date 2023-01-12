from unittest import TestCase

from project_tools.classes import GuitarNotes

class NotesClassTest(TestCase):

    def test_valid_root_note(self):
        """ Check valid input in object.set_root_note
            method 
        """
        # Test with uppercase letters
        new_object = GuitarNotes()
        note = 'A'
        self.assertEqual(note, new_object.set_root_note(note))
        second_note = 'F#'
        self.assertEqual(second_note, new_object.set_root_note(second_note))
        # Test with lowercase letters
        lower_case_note = 'd#'
        self.assertEqual('D#', new_object.set_root_note(lower_case_note))


    def test_invalid_root_note_raise_error(self):
        """ Check invalid input in object.set_root_note
            method 
        """
        new_object = GuitarNotes()
        wrong_note = ''
        with self.assertRaises(ValueError):
            new_object.set_root_note(wrong_note)

    def test_valid_minor_chord(self):
        """ Check valid input in object.show_chords
            method
        """
        new_object = GuitarNotes()
        chord = new_object.show_chord('f', 'major')
        self.assertEqual(chord, ['F', 'A', 'C'])

    def test_invalid_chord(self):
        """ Check that object.show_chord
            raise an error when input is invalid 
        """
        new_object = GuitarNotes()
        with self.assertRaises(ValueError):
            new_object.show_chord('', '')
        with self.assertRaises(KeyError):
            new_object.show_chord('b', 'mjor')

    def test_scale_with_valid_input(self):
        """ Check that method return valid list
            of notes, that form scale.
            And scale starts with a root note
        """
        new_object = GuitarNotes()
        c_note = 'C'
        c_maj_scale = new_object.show_scale(c_note, 'major')
        self.assertEqual(c_maj_scale[0], c_note)
        self.assertEqual(c_maj_scale, ['C', 'D', 'E', 'F', 'G', 'A', 'B'])

        a_note = 'A'
        a_min_scale = new_object.show_scale(a_note, 'minor')
        self.assertEqual(a_min_scale[0], a_note)
        self.assertEqual(a_min_scale, ['A', 'B', 'C', 'D', 'E', 'F', 'G'])

    def test_scale_with_invalid_input(self):
        """ Check that method object.show_scale 
            raise an error with an invalid input
        """
        new_object = GuitarNotes()
        c_note = 'C##'
        with self.assertRaises(ValueError):
            new_object.show_scale(c_note, 'major')
        
        d_note = "D"
        with self.assertRaises(KeyError):
            new_object.show_scale(d_note, 'majo')

