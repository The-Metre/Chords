class GuitarNotes:

    # All music tones names
    __notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

    # Standart guitar tuning
    __default_tuning = ['E', 'B', 'G', 'D', 'A', 'E']

    # Contain indexes of notes for each chord type
    __chord_formula = {
                'major' : [0, 4, 7],
                'minor' : [0, 3, 7],
                '7': [0, 4, 7, 10],
                'sus2': [0, 2, 7],
                'sus4': [0, 5, 7]
    }

    # Contain indexes of notes for each scale type
    __scale_formula = {
            'major' :  [0, 2, 4, 5, 7, 9, 11],
            'minor' : [0, 2, 3, 5, 7, 8, 10],
            'major penta': [0, 2, 4, 7, 9],
            'minor penta': [0, 3, 5, 7, 10]
    }

    def __init__(self, strings_list: list[str] = __default_tuning) -> None:
        self.set_guitar_fretboard(strings_list)


    def show_scale(self, root_note:str, scale_type:str) -> list[str]:
        """ Return a list with notes thtat contain specific scale
            if either root_note or_scale_type is invalid
            the function will raise an error
        """
        root_note = self.set_root_note(root_note)
        scale = self.string_tuning(root_note)

        if scale_type.lower() not in self.__scale_formula:
            raise KeyError(f'Invalid scale type: {scale_type}')
        
        scale_notes = self.__scale_formula[scale_type.lower()]
        return [note for note in scale if scale.index(note) in scale_notes]



    def show_chord(self, root_note:str, chord_type:str) -> list[str]:
        """ Return a list with notes that contain specific chord type
            if either root_note or chord_type is invalid,
            the function will raise an error
        """
        root_note = self.set_root_note(root_note)
        scale = self.string_tuning(root_note)

        if chord_type.lower() not in self.__chord_formula:
            raise KeyError(f'Invalid chord type: {chord_type}')

        chord = self.__chord_formula[chord_type.lower()]
        return [note for note in scale if scale.index(note) in chord]

    def set_root_note(self, root_note:str) -> list[str]:
        """ Return a valid root note from notes list,
            if note doesn't exist raise an error 
        """
        if root_note.upper() not in self.__notes:
            raise ValueError(f'Incorrect root note: "{root_note}"!')
        return root_note.upper()

    def string_tuning(self, fretnote: str) -> list[str]:
        """ Set a string of notes, first element will
            be a note from the choosen fret
        """
        note = self.set_root_note(fretnote)
        note_index = self.__notes.index(note)
        return self.__notes[note_index:] + self.__notes[:note_index]

    def set_guitar_fretboard(self, strings_list: list[str]) -> list[list[str]]:
        """ Form the guitar fretboard with provided strings """
        self.guitar_fretboard = [self.string_tuning(item) for item in strings_list]


    

def main():
    pass

if __name__ == '__main__':
    main()