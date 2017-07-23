# Two strings for the greedy string tiling algorithm



#            0          1    2     3   4        5      6  7       8          9   10  11 12       13   14         15  16      17 18     19    20     21       22    23  24        25    26  27    28   29
# string 1:  surprising many trump had remained silent on twitter throughout the day on thursday when washington was riveted by comeys first public comments since the president fired him early last month
# string 2a: surprising many trump had remained silent on aaaaaaa bbbbbbbbbb ccc day on thursday when washington ddd eeeeeee ff gggggg hhhhh public comments since the president iiiii kkk early last month
# string 2b: aaaaaaaaaa bbbb ccccc ddd eeeeeeee ffffff gg hhhhhhh iiiiiiiiii jjj kkk ll mmmmmmmm nnnn oooooooooo ppp qqqqqqq rr ssssss ttttt uuuuuu vvvvvvvv wwwww xxx yyyyyyyyy zzzzz 111 22222 3333 33333

# (t, p, length)
# ( 0,  0, 7)
# ( 1,  1, 6)
# ( 2,  2, 5)
# (10, 10, 5)
# (20, 20, 5)
# (27, 27, 3)


strings = [
    [
        'surprising many trump had remained silent on twitter throughout the day on thursday when washington was riveted by comeys first public comments since the president fired him early last month',

        'surprising many trump ddd remained silent on twitter throughout jjj day on thursday when oooooooooo was riveted by comeys first public comments since xxx yyyyyyyyy zzzzz 111 22222 last month'
    ],
    [
        'Surprising many Trump had remained silent on Twitter throughout the day on Thursday when Washington was ' \
        'riveted by Comeys first public comments since the president fired him early last month Comey said he believed Trump terminated ' \
        'him over the FBIs investigation into Russian meddling in the 2016 presidential election His testimony included the ' \
        'revelation that he authorized a close friend to share with the press a memo describing a meeting with Trump in which ' \
        'the president allegedly asked him to let go of the probe into former national security adviser Michael Flynn I didnt ' \
        'do it myself for a variety of reasons but I asked him to because I thought that might prompt the appointment of a ' \
        'special counsel Comey said Trumps team pounced on the comments In a statement read to reporters Marc  ' \
        'the presidents outside attorney slammed the leak and categorically denied that Trump ever directed or suggested' \
        'that Comey stop investigating anyone Today Mr Comey admitted that he unilaterally and surreptitiously made ' \
        'unauthorized disclosures to the press of privileged communications with the president Kasowitz said Comey said one of ' \
        'the reasons he felt compelled to speak out was the administrations shifting rationale for his firing Originally ' \
        'pointing the finger at his handling of the Hillary Clinton email server investigation the White House later said Comey ' \
        'had mismanaged the FBI and lost the faith of rank-and-file agents Trump also told NBC News that Comey was fired over ' \
        'the Russia probe The administration chose to defame me and more importantly the FBI by saying that the organization ' \
        'was in disarray that it was poorly run Comey told the Senate Intelligence penal Those were lies plain and simple',

        'President Donald Trump claimed total and complete vindication the day after former FBI Director James Comey testified ' \
        'on Capitol Hill tweeting his first response to the bombshell testimony after spending all of Thursday off his social media ' \
        'site of choice Trumps comment tracks with Republican talking points about the hearing where the Republican ' \
        'National Committee and White House urged surrogates to emphasize the fact that Comey clearly said the President was ' \
        'never an explicit subject of the Russia probe during his time at the FBI But Comeys testimony about the President was ' \
        'also damaging The former FBI director said Trumps private comments urging him to drop the probe into former national ' \
        'security adviser Michael Flynn led him to tell his Justice Department colleagues they needed to be careful And he ' \
        'said multiple times that he choose to take detailed notes about his interactions with Trump because he worried the ' \
        'White House and President would lie about them if he didnt. Despite so many false statements and lies, total and complete ' \
        'vindication and WOW, Comey is a leaker Trump tweeted Friday morning Trump fired Comey in May, setting off a series ' \
        'of events that eventually led the career law enforcement official to sit before senators on Thursday. And Fridays ' \
        'message on Twitter was the President in effect, accusing Comey of perjury because the former FBI director was under oath during ' \
        'the Senate intelligence committee hearing The White House initially blamed Comeys firing on the way he handled the ' \
        'Hillary Clinton email investigation during the 2016 election But once that excuse fell apart Trump himself said he fired ' \
        'the former FBI director over the FBI probe That Comey said worried him Its my judgment that I was fired because of the ' \
        'Russia investigation Comey said I was fired in some way to change or the endeavor was to change the way the Russia ' \
        'investigation was being conducted Republicans who have been pushing the need to punish leakers for months have also ' \
        'jumped on the fact that Comey provided the content of a memo regarding meetings between himself and the President to a ' \
        'friend who then disseminated the information to the media Trumps outside lawyer insisted Thursday that it was Comey ' \
        'who lied when he detailed conversations between himself and the President raising the accusation that Comey committed ' \
        'perjury while testifying under oath Marc Kasowitz Trumps recently hired outside counsel slammed Comey for unilaterally ' \
        'and surreptitiously disseminating the content of his conversations with Trump arguing that information was privileged A ' \
        'number of legal scholars disagree with Kasowitzs assessment including John Dean who served as White House counsel ' \
        'in the Nixon administration This is not privileged information Dean said bluntly Trumps top aides and advisers ' \
        'successfully kept the president off Twitter during the Comey hearing something they told reporters they were hoping to do ' \
        'Trump was asked about Comeys testimony multiple times during a meeting with governors and mayors but ignored all the ' \
        'questions The President will likely be asked directly about the former FBI directors testimony on Friday when he takes ' \
        'formal questions for the first time in three weeks during a joint press conference in the Rose Garden with Romanian President ' \
        'Klaus Iohanni'
    ]
]
