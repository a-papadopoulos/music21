# -*- coding: utf-8 -*-
import re
import unittest
from music21 import freezeThaw


class Test(unittest.TestCase):

    # When `maxDiff` is None, `assertMultiLineEqual()` provides better errors.
    maxDiff = None

    def runTest(self):
        pass

    def testMetadataLoadCorpus(self):
        from music21 import converter
        from music21.musicxml import testFiles as mTF

        c = converter.parse(mTF.mozartTrioK581Excerpt)  # @UndefinedVariable
        md = c.metadata

        self.assertEqual(md.movementNumber, '3')
        self.assertEqual(
            md.movementName, 'Menuetto (Excerpt from Second Trio)')
        self.assertEqual(md.title, 'Quintet for Clarinet and Strings')
        self.assertEqual(md.number, 'K. 581')
        # get contributors directly from Metadata interface
        self.assertEqual(md.composer, 'Wolfgang Amadeus Mozart')

        c = converter.parse(mTF.binchoisMagnificat)  # @UndefinedVariable
        md = c.metadata
        self.assertEqual(md.composer, 'Gilles Binchois')

    def testJSONSerializationMetadata(self):
        from music21 import converter
        from music21.musicxml import testFiles as mTF
        from music21 import metadata

        md = metadata.Metadata(
            title='Concerto in F',
            date='2010',
            composer='Frank',
            )
        #environLocal.printDebug([str(md.json)])
        self.assertEqual(md.composer, 'Frank')

        #md.jsonPrint()

        mdNew = metadata.Metadata()

        jsonString = freezeThaw.JSONFreezer(md).json
        freezeThaw.JSONThawer(mdNew).json = jsonString

        self.assertEqual(mdNew.date, '2010/--/--')
        self.assertEqual(mdNew.composer, 'Frank')

        self.assertEqual(mdNew.title, 'Concerto in F')

        # test getting meta data from an imported source
        c = converter.parse(mTF.mozartTrioK581Excerpt)  # @UndefinedVariable
        md = c.metadata

        self.assertEqual(md.movementNumber, '3')
        self.assertEqual(
            md.movementName, 'Menuetto (Excerpt from Second Trio)')
        self.assertEqual(md.title, 'Quintet for Clarinet and Strings')
        self.assertEqual(md.number, 'K. 581')
        self.assertEqual(md.composer, 'Wolfgang Amadeus Mozart')

        # convert to json and see if data is still there
        #md.jsonPrint()
        mdNew = metadata.Metadata()

        jsonString = freezeThaw.JSONFreezer(md).json
        freezeThaw.JSONThawer(mdNew).json = jsonString

        self.assertEqual(mdNew.movementNumber, '3')
        self.assertEqual(
            mdNew.movementName, 'Menuetto (Excerpt from Second Trio)')
        self.assertEqual(mdNew.title, 'Quintet for Clarinet and Strings')
        self.assertEqual(mdNew.number, 'K. 581')
        self.assertEqual(mdNew.composer, 'Wolfgang Amadeus Mozart')

    def testRichMetadata01(self):
        from music21 import corpus
        from music21 import metadata

        score = corpus.parse('jactatur')
        self.assertEqual(score.metadata.composer, 'Johannes Ciconia')

        richMetadata = metadata.RichMetadata()
        richMetadata.merge(score.metadata)

        self.assertEqual(richMetadata.composer, 'Johannes Ciconia')
        # update richMetadata with stream
        richMetadata.update(score)

        self.assertEqual(
            richMetadata.keySignatureFirst,
            '<music21.key.Key of F major>',
            )

        self.assertEqual(str(richMetadata.timeSignatureFirst), '2/4')

        rmdNew = metadata.RichMetadata()

        jsonString = freezeThaw.JSONFreezer(richMetadata).json
        freezeThaw.JSONThawer(rmdNew).json = jsonString

        self.assertEqual(rmdNew.composer, 'Johannes Ciconia')

        self.assertEqual(str(rmdNew.timeSignatureFirst), '2/4')
        self.assertEqual(
            str(rmdNew.keySignatureFirst),
            '<music21.key.Key of F major>',
            )

        score = corpus.parse('bwv66.6')
        richMetadata = metadata.RichMetadata()
        richMetadata.merge(score.metadata)

        richMetadata.update(score)
        self.assertEqual(
            str(richMetadata.keySignatureFirst),
            '<music21.key.Key of f# minor>',
            )
        self.assertEqual(str(richMetadata.timeSignatureFirst), '4/4')

        jsonString = freezeThaw.JSONFreezer(richMetadata).json
        freezeThaw.JSONThawer(rmdNew).json = jsonString

        self.assertEqual(str(rmdNew.timeSignatureFirst), '4/4')
        self.assertEqual(
            str(rmdNew.keySignatureFirst),
            '<music21.key.Key of f# minor>',
            )

    def testWorkIds(self):
        from music21 import corpus
        from music21 import metadata

        opus = corpus.parse('essenFolksong/teste')
        self.assertEqual(len(opus), 8)

        score = opus.getScoreByNumber(4)
        self.assertEqual(score.metadata.localeOfComposition,
            'Asien, Ostasien, China, Sichuan')

        richMetadata = metadata.RichMetadata()
        richMetadata.merge(score.metadata)
        richMetadata.update(score)

        self.assertEqual(richMetadata.localeOfComposition,
            'Asien, Ostasien, China, Sichuan')

    def testMetadataSearch(self):
        from music21 import corpus
        score = corpus.parse('ciconia')
        self.assertEqual(
            score.metadata.search(
                'quod',
                field='title',
                ),
            (True, 'title'),
            )
        self.assertEqual(
            score.metadata.search(
                'qu.d',
                field='title',
                ),
            (True, 'title'),
            )
        self.assertEqual(
            score.metadata.search(
                re.compile('(.*)canon(.*)'),
                ),
            (True, 'movementName'),
            )

    def testRichMetadata02(self):
        from music21 import VERSION
        from music21 import corpus
        from music21 import metadata
        import textwrap
        
        score = corpus.parse('bwv66.6')
        richMetadata = metadata.RichMetadata()
        richMetadata.merge(score.metadata)
        richMetadata.update(score)
        self.assertEqual(richMetadata.noteCount, 165)
        self.assertEqual(richMetadata.quarterLength, 36.0)
        self.assertMultiLineEqual(
            freezeThaw.JSONFreezer(richMetadata).prettyJson.strip(),
            textwrap.dedent('''
                {
                    "__attr__": {
                        "_urls": [],
                        "_workIds": {
                            "movementName": {
                                "__attr__": {
                                    "_data": "bwv66.6.mxl"
                                },
                                "__class__": "music21.metadata.primitives.Text"
                            }
                        },
                        "ambitus": [
                            34,
                            "m7",
                            "F#2",
                            "E5"
                        ],
                        "contributors": [],
                        "keySignatureFirst": "<music21.key.Key of f# minor>",
                        "keySignatures": [
                            "<music21.key.Key of f# minor>"
                        ],
                        "noteCount": 165,
                        "numberOfParts": 4,
                        "pitchHighest": "E5",
                        "pitchLowest": "F#2",
                        "quarterLength": 36.0,
                        "sourcePath": "bach/bwv66.6.mxl",
                        "tempos": [],
                        "timeSignatureFirst": "4/4",
                        "timeSignatures": [
                            "4/4"
                        ]
                    },
                    "__class__": "music21.metadata.RichMetadata",
                    "__version__": [
                        %d,
                        %d,
                        %d
                    ]
                }''' % (VERSION[0], VERSION[1], VERSION[2]),
                ).strip())

#------------------------------------------------------------------------------

if __name__ == "__main__":
    import music21
    music21.mainTest(Test, 'noDocTest')
