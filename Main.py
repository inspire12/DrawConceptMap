
import LDAExtractConcept
#-*- coding: utf-8 -*-
def main():
    video_id = "bxe2T-V8XRs"
    video_list_id = "PLiaHhY2iBX9hdHaRr6b7XevZtgZRa1PoU"
    #instance = ExtractConcept.ExtractConcept()

    #concept = instance.Extract_Concept_1(instance.Extract_subcript(video_id))
    #print(concept)

    playlist_url = 'https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV'
    URLs= LDAExtractConcept.get_all_URLs(playlist_url)
    video_IDs = LDAExtractConcept.get_videoIDs(URLs)
    print(LDAExtractConcept.LDA(video_IDs, 7, 10))


if __name__ == "__main__":
    main()