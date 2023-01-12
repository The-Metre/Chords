class GuitarNotes:
    __notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

    __default_tuning = ['E', 'B', 'G', 'D', 'A', 'E']

    __chord_formula = {
                'major' : [0, 4, 7],
                'minor' : [0, 3, 7],
                '7': [0, 4, 7, 10],
                'sus2': [0, 2, 7],
                'sus4': [0, 5, 7]
    }

    def __init__(self, strings_list: list[str] = __default_tuning) -> None:
        self.set_guitar_fretboard(strings_list)

    def set_root_note(self, root_note:str) -> list[str]:
        if root_note.upper() not in self.__notes:
            raise ValueError('Incorrect root note!')
        return root_note.upper()

    def show_the_scale(self, root_note:str, chord_type:str) -> list[str]:
        root_note = self.set_root_note(root_note)
        scale = self.string_tuning(root_note)

        if chord_type.lower() not in self.__chord_formula:
            raise KeyError(f'Invalid chord type: {chord_type}')

        chord = self.__chord_formula[chord_type.lower()]
        return [note for note in scale if scale.index(note) in chord]


    @classmethod
    def string_tuning(cls, fretnote: str) -> list[str]:
        index = cls.__notes.index(fretnote.upper())
        return cls.__notes[index:] + cls.__notes[:index]

    def set_guitar_fretboard(self, strings_list: list[str]) -> list[list[str]]:
        """ Form the guitar fretboard with provided strings """
        self.guitar_fretboard = [self.string_tuning(item) for item in strings_list]


    

def main():
    pass

if __name__ == '__main__':
    main()