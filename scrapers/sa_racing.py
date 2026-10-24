from models import Horse, Race

class SARacingDataProvider:
    @classmethod
    def get_live_greyville_card(cls):
        # Races 4 through 8 currently running tonight at Greyville
        return [
            Race("GRV-20261023-R4", "Hollywoodbets Greyville", 4, "Bet With Tote Maiden Plate", "17:25", 1000, "Polytrack", "Standard", [
                Horse(1, "J Lordi", 1, 78, "Kabelo Matsunyane", "Kelly Mitchley", 60.0, "2-3-2-2", True, 21, 2.20, 0.17, 0.16),
                Horse(2, "Rachel's Boy", 2, 73, "Anaas Mosaheb", "Garth Puller", 58.5, "4-5-3-4", False, 35, 5.50, 0.14, 0.13),
                Horse(3, "Queraristinyferari", 3, 70, "Serino Moodley", "Dennis Bosch", 57.0, "6-4-5-3", False, 14, 8.00, 0.13, 0.12),
                Horse(4, "Little Lollita", 4, 68, "Cole Dicken", "Wendy Whitehead", 56.0, "5-6-7-4", False, 42, 12.0, 0.12, 0.14),
                Horse(5, "Belligerent", 5, 66, "Calvin Habib", "Gareth van Zyl", 56.0, "7-8-6-5", False, 28, 15.0, 0.18, 0.15),
            ]),
            Race("GRV-20261023-R5", "Hollywoodbets Greyville", 5, "Pinkdrive Apprentice C Stakes", "18:00", 1000, "Polytrack", "Standard", [
                Horse(1, "Chara Sands", 1, 84, "Divesh Ramkhalawon", "Michael Roberts", 60.0, "3-1-4-2", True, 28, 3.50, 0.15, 0.14),
                Horse(2, "Smorgasbord", 2, 82, "Cole Dicken", "Wendy Whitehead", 59.0, "5-4-3-6", False, 49, 7.00, 0.12, 0.14),
                Horse(3, "B Fiftytwo", 3, 86, "Damyan Pillay", "Wendy Whitehead", 61.5, "1-2-1-3", True, 21, 2.80, 0.16, 0.14),
                Horse(4, "Quarter Master", 4, 78, "Shalton Sesingi", "Robbie Hill", 56.5, "6-5-4-3", False, 35, 10.0, 0.11, 0.12),
                Horse(5, "Mojo Man", 5, 80, "Anaas Mosaheb", "Wendy Whitehead", 58.0, "2-3-5-4", True, 14, 5.00, 0.14, 0.14),
                Horse(6, "Time To Fire", 6, 76, "Sifisokuhle Bungane", "Warrick Marwing", 55.0, "4-6-7-5", False, 42, 16.0, 0.10, 0.11),
            ]),
            Race("GRV-20261023-R6", "Hollywoodbets Greyville", 6, "Online Form Guide Gallop TV D Stakes", "18:35", 2000, "Polytrack", "Standard", [
                Horse(1, "Satellite World", 1, 75, "Tristan Godden", "Kumaran Naidoo", 56.0, "3-4-2-5", False, 28, 6.00, 0.13, 0.12),
                Horse(2, "Twocantango", 2, 72, "Calvin Habib", "Gareth van Zyl", 54.5, "5-6-4-3", False, 35, 8.50, 0.18, 0.15),
                Horse(3, "Preux Chavalier", 3, 82, "Keagan de Melo", "Dean Kannemeyer", 60.0, "1-2-1-2", True, 21, 2.25, 0.19, 0.18),
                Horse(5, "Mohandas", 5, 74, "Serino Moodley", "Dennis Bosch", 55.5, "4-3-5-4", False, 14, 7.50, 0.13, 0.12),
                Horse(6, "Record High", 6, 78, "Kabelo Matsunyane", "Kelly Mitchley", 58.0, "2-1-3-4", True, 28, 4.00, 0.17, 0.16),
                Horse(7, "Dancing On A Cloud", 7, 70, "Anaas Mosaheb", "Garth Puller", 53.0, "6-7-5-6", False, 42, 14.0, 0.14, 0.13),
            ]),
            Race("GRV-20261023-R7", "Hollywoodbets Greyville", 7, "Lucky Fish Fortune Cup C Stakes", "19:10", 1600, "Polytrack", "Standard", [
                Horse(1, "Beach Palace", 1, 80, "Anaas Mosaheb", "Frikkie Greyling", 57.5, "2-4-3-1", True, 21, 4.50, 0.14, 0.12),
                Horse(2, "Pied Piper", 2, 83, "Kabelo Matsunyane", "Wengesai Masawi", 59.0, "1-2-1-3", True, 28, 3.25, 0.17, 0.14),
                Horse(3, "High Queue", 3, 78, "Qiniso Ngcobo", "Wengesai Masawi", 56.5, "4-3-2-5", False, 35, 6.50, 0.12, 0.14),
                Horse(4, "Master of Destiny", 4, 76, "Calvin Habib", "Gareth van Zyl", 55.0, "5-5-4-3", False, 14, 8.00, 0.18, 0.15),
                Horse(5, "Syrian Sovereign", 5, 75, "Keagan de Melo", "Dean Kannemeyer", 54.5, "3-6-5-4", False, 42, 7.00, 0.19, 0.18),
            ]),
            Race("GRV-20261023-R8", "Hollywoodbets Greyville", 8, "Hollywoodbets Bright Future Apprentice D Stakes", "19:45", 1200, "Polytrack", "Standard", [
                Horse(1, "Kaapse Klopse", 1, 81, "Anaas Mosaheb", "Matthys Odendaal", 60.0, "1-3-2-1", True, 21, 3.00, 0.14, 0.14),
                Horse(2, "Xiphos", 2, 76, "Divesh Ramkhalawon", "Frikkie Greyling", 57.0, "3-2-4-5", False, 35, 5.50, 0.15, 0.12),
                Horse(3, "Stage One", 3, 73, "Sifisokuhle Bungane", "Warrick Marwing", 55.0, "5-4-6-3", False, 28, 8.50, 0.10, 0.11),
                Horse(4, "Commanding", 4, 78, "Jacey Botes", "Glen Kotzen", 58.5, "2-1-3-4", True, 14, 4.00, 0.13, 0.17),
                Horse(5, "Final Destiny", 5, 71, "Shalton Sesingi", "Robbie Hill", 54.0, "6-5-7-4", False, 42, 12.0, 0.11, 0.12),
            ]),
        ]
