from django.core.management.base import BaseCommand
from apps.treks.models import Trek, Itinerary, IncludedItem, ExcludedItem, MapCoordinate ,TrekImage
from decimal import Decimal
from django.core.files import File
from pathlib import Path
from django.db.utils import IntegrityError
import os
import sys

# --- CONFIGURATION VARIABLES ---
# Base path where your trek image folders (abc, everest-base-camp, etc.) are located.
MEDIA_BASE = Path('D:/nepaltrekconnect/backend/media/trek_images/') 

# Ensure the titles here EXACTLY match the title defined in Trek.objects.create()
TREK_FOLDERS = {
    "abc": 'Annapurna Base Camp Trek - 10 Days to the Annapurna Sanctuary',
    "everest-base-camp": 'Everest Base Camp Trek - 14 Days Journey to the World\'s Highest Peak',
    "uppermustang": 'Upper Mustang Trek - 17 Days: Ancient Forbidden Kingdom of Lo',
    "langtang": 'Langtang Valley Trek - 10 Days: Valley of Glaciers',
    "manaslu": 'Manaslu Circuit Trek - 15 Days via Larkya La Pass',
    "mardihimaltrek": 'Mardi Himal Trek - 8 Days: Close-Up Views of Mount Fishtail', 
    "shortabctrek": 'Annapurna Circuit Trek (Short) - 15 Days via Thorong La Pass', 
    "rara": 'Rara Lake Trek - 15 Days: Wilderness Trek to Nepal\'s Largest Lake', 
    "poonhill": 'Ghorepani Poon Hill Trek - 5 Days: Sunrise over the Himalayas' 
}
# --- END CONFIGURATION ---

class Command(BaseCommand):
    help = 'Load initial trek data and link images.'

    def handle(self, *args, **options):
        
        # --- 0. PRE-CHECK ---
        if not MEDIA_BASE.exists():
            self.stdout.write(self.style.ERROR(f"FATAL ERROR: MEDIA_BASE path does not exist: {MEDIA_BASE}"))
            sys.exit(1)
        
        self.stdout.write(self.style.WARNING("Starting data loading and image linking process..."))
        
        # --- 1. DATA CREATION SECTION (All the Trek, Itinerary, etc. objects must be created here) ---
        
        try:
            # --- 1. ANNAPURNA BASE CAMP TREK (ABC) ---
            self.stdout.write("--- Creating ABC Trek Data ---")
            abc = Trek.objects.create(
                title="Annapurna Base Camp Trek - 10 Days to the Annapurna Sanctuary",
                slug="annapurna-base-camp-trek-10-days",
                short_description="Trek into the heart of the Annapurna Massif, reaching the famous Annapurna Sanctuary (ABC). Experience Gurung and Magar culture, dense rhododendron forests, and a spectacular 360° panorama of the Himalayas.",
                long_description="The Annapurna Base Camp (ABC) trek is one of the most rewarding short treks, leading you into a natural amphitheater of towering peaks including Annapurna I (8,091m), Machhapuchhre (Fishtail), and Hiunchuli. The journey begins with a drive from Pokhara and ascends through charming Gurung villages and lush sub-tropical forest before emerging into the high alpine sanctuary.",
                location="Pokhara, Annapurna Region, Himalayas, Nepal",
                start_point="Pokhara",
                latitude=Decimal('28.5385'),
                longitude=Decimal('83.8860'),
                
                duration_days=10,
                duration_nights=9,
                difficulty="moderate",
                max_altitude=4130,
                max_altitude_feet=13550,
                best_season="spring_autumn",
                price_usd=Decimal('899.00'),
                discount_percentage=5,
                is_featured=True,
                is_popular=True,
                meta_description="Book the 10-Day Annapurna Base Camp (ABC) Trek from Pokhara. Reach the Annapurna Sanctuary and witness a 360-degree view of Annapurna I, Machhapuchhre, and more.",
                meta_keywords="annapurna base camp trek, abc trek, annapurna sanctuary, nepal trekking, machhapuchhre, pokhara trek, gurung culture",
                image_keywords="Annapurna Base Camp, ABC sign, Machhapuchhre (Fishtail) Peak, Modi Khola Valley, Bamboo forest, Gurung village, hot springs, rhododendron forest"
            )

            # Add itinerary for ABC (Pokhara start/end)
            abc_days = [
                (1, "Arrival in Kathmandu & Transfer to Pokhara", "Airport pickup at TIA, followed by transfer to Pokhara via tourist bus (included) or domestic flight (excluded). Hotel check-in and trek briefing in Pokhara.", "820m", "6-8 hours (drive)", "Hotel in Pokhara"),
                (2, "Drive to Nayapul & Trek to Tikhedhunga", "Morning drive to Nayapul (trek start point). Begin trekking through villages, enjoying the lower Modi Khola valley. Overnight stop at Tikhedhunga.", "1,540m", "4-5 hours", "Tea House"),
                (3, "Trek to Ghorepani", "Ascend the famous stone staircase (3200 steps) to Ulleri. Continue through rhododendron forests to the Magar village of Ghorepani.", "2,860m", "6-7 hours", "Tea House"),
                (4, "Hike to Poon Hill & Trek to Tadapani", "Early morning hike to Poon Hill (3210m) for sunrise over the Dhaulagiri and Annapurna ranges. Return for breakfast and trek to Tadapani.", "2,630m", "5-6 hours", "Tea House"),
                (5, "Trek to Chomrong", "Descend to Chomrong Khola and cross the river. Climb up to Sinuwa and continue trekking through bamboo and rhododendron forests to Dovan.", "2,600m", "5-6 hours", "Tea House"),
                (6, "Trek to Dovan", "Descend to Chomrong Khola and cross the river. Climb up to Sinuwa and continue trekking through bamboo and rhododendron forests to Dovan.", "2,600m", "5-6 hours", "Tea House"),
                (7, "Trek to Machhapuchhre Base Camp (MBC)", "The trail enters the 'Gateway to the Sanctuary' with no permanent settlements above Dovan. Pass through Himalaya and Deurali before reaching MBC.", "3,700m", "5-6 hours", "Tea House"),
                (8, "Trek to Annapurna Base Camp (ABC)", "A short day's climb into the Annapurna Sanctuary. Witness the 360-degree panorama of mountains surrounding ABC. Explore the base camp.", "4,130m", "2-3 hours", "Tea House"),
                (9, "ABC to Bamboo", "Watch the stunning sunrise from the sanctuary. Start the long descent back, rapidly losing altitude to Bamboo.", "2,340m", "7-8 hours", "Tea House"),
                (10, "Bamboo to Jhinu Danda & Drive to Pokhara", "Trek to Jhinu Danda. You can enjoy the natural hot springs (optional). Take a local jeep/bus drive from Jhinu Danda back to Pokhara. Farewell dinner and overnight stay.", "820m", "4-5 hours (trek) + 3 hours (drive)", "Hotel in Pokhara"),
            ]

            for day_num, title, desc, alt, hours, acc in abc_days:
                Itinerary.objects.create(
                    trek=abc, day_number=day_num, title=title, description=desc, altitude=alt, trekking_hours=hours, accommodation=acc, meals_included="Breakfast, Lunch, Dinner"
                )

            # Add included items for ABC
            abc_included = [
                "Kathmandu to Pokhara transportation (Tourist Bus - included)",
                "Pokhara to Nayapul/Jhinu Danda to Pokhara transfer (Private Vehicle/Jeep)",
                "TIMS Card (Trekkers' Information Management System) and ACAP (Annapurna Conservation Area Permit)",
                "Experienced, government-licensed, English-speaking trekking guide",
                "Porter service (1 porter for 2 trekkers, maximum weight 20kg)",
                "9 nights accommodation during the trek (best available tea houses/lodges)",
                "3 meals a day (Breakfast, Lunch, Dinner) during the trek",
                "Accommodation in Pokhara (Day 1, 10 - Standard 3-star hotel with breakfast)",
                "Staff costs (insurance, salary, equipment, food, and accommodation for all staff)",
                "Comprehensive first aid kit",
                "Company T-shirt, trekking map, and certificate of completion",
                "Farewell dinner in Pokhara"
            ]

            for idx, item in enumerate(abc_included, 1):
                IncludedItem.objects.create(trek=abc, item=item, order=idx)

            # Add excluded items for ABC
            abc_excluded = [
                "International airfare to/from Kathmandu",
                "Nepal entry visa fee (obtainable on arrival at TIA)",
                "Domestic flight from Kathmandu to Pokhara (Approx. USD $100-120)",
                "Travel and rescue insurance (mandatory and must cover high altitude rescue)",
                "Personal expenses (bottled water, soft drinks, alcoholic beverages, phone calls, laundry, Wi-Fi/battery charging)",
                "Showers and hot water charges at tea houses",
                "Tips for guide and porter (expected)",
                "Extra costs due to delays, cancellations, or changes to the itinerary beyond our control (e.g., weather)",
                "All costs in Kathmandu (except airport transfer)"
            ]

            for idx, item in enumerate(abc_excluded, 1):
                ExcludedItem.objects.create(trek=abc, item=item, order=idx)

            # Add map coordinates for ABC
            abc_coords = [
                ("Pokhara", Decimal('28.2096'), Decimal('83.9856')),
                ("Nayapul", Decimal('28.3244'), Decimal('83.7744')),
                ("Ghorepani", Decimal('28.3970'), Decimal('83.7020')),
                ("Chomrong", Decimal('28.3923'), Decimal('83.8440')),
                ("Machhapuchhre Base Camp (MBC)", Decimal('28.4795'), Decimal('83.8967')),
                ("Annapurna Base Camp (ABC)", Decimal('28.5385'), Decimal('83.8860')),
            ]

            for idx, (name, lat, lng) in enumerate(abc_coords, 1):
                MapCoordinate.objects.create(trek=abc, name=name, latitude=lat, longitude=lng, order=idx)
            
            self.stdout.write(self.style.SUCCESS("✅ ABC Trek data loaded."))


            # --- 2. GHOREPANI POON HILL TREK ---
            self.stdout.write("--- Creating Poon Hill Trek Data ---")
            pph = Trek.objects.create(
                title="Ghorepani Poon Hill Trek - 5 Days: Sunrise over the Himalayas",
                slug="ghorepani-poon-hill-trek-5-days",
                short_description="A perfect introduction to trekking in Nepal. This short, easy-to-moderate trek offers magnificent sunrise views over the Dhaulagiri and Annapurna ranges from Poon Hill, complemented by the rich culture of Gurung and Magar villages.",
                long_description="Ideal for beginners, the Ghorepani Poon Hill trek is famous for the stunning panoramic views from Poon Hill (3,210m). The trail is well-trodden, passing through dense rhododendron forests and traditional villages, making it a highly accessible and culturally rich experience in the Annapurna foothills.",
                location="Pokhara, Annapurna Region, Himalayas, Nepal",
                start_point="Pokhara",
                latitude=Decimal('28.3750'),
                longitude=Decimal('83.6920'),
                duration_days=5,
                duration_nights=4,
                difficulty="easy_moderate",
                max_altitude=3210,
                max_altitude_feet=10531,
                best_season="spring_autumn",
                price_usd=Decimal('499.00'),
                discount_percentage=0,
                is_featured=False,
                is_popular=True,
                meta_description="Book the 5-Day Ghorepani Poon Hill Trek from Pokhara. Enjoy the best sunrise in Nepal over Dhaulagiri and Annapurna. Easy to moderate difficulty.",
                meta_keywords="poon hill trek, ghorepani trek, short nepal trek, easy himalaya trek, poon hill sunrise, gurung village, pokhara trekking",
                image_keywords="Poon Hill sunrise, Annapurna South view, Dhaulagiri view, Ghorepani village, rhododendron flower, Gurung mother, stone staircase"
            )

            # Add itinerary for PPH (Pokhara start/end)
            pph_days = [
                (1, "Arrival in Kathmandu & Transfer to Pokhara", "Airport pickup at TIA, followed by transfer to Pokhara via tourist bus (included) or domestic flight (excluded). Hotel check-in and trek briefing in Pokhara.", "820m", "6-8 hours (drive)", "Hotel in Pokhara"),
                (2, "Drive to Nayapul & Trek to Tikhedhunga", "Morning drive to Nayapul (trek start point). Begin trekking through Birethanti. Follow the river and arrive at Tikhedhunga.", "1,540m", "4-5 hours", "Tea House"),
                (3, "Trek to Ghorepani", "The most challenging day: ascend the famously steep stone steps to Ulleri, then continue through beautiful rhododendron forest to Ghorepani, a large Magar village.", "2,860m", "6-7 hours", "Tea House"),
                (4, "Hike to Poon Hill & Trek to Ghandruk", "Pre-dawn hike to Poon Hill (3210m) for the iconic sunrise view. Return for breakfast. Trek through dense forest to the beautiful, large Gurung village of Ghandruk.", "2,012m", "6-7 hours", "Tea House"),
                (5, "Trek to Nayapul & Drive to Pokhara", "A gentle descent through terraced fields and villages to Nayapul. Drive from Nayapul back to Pokhara. End of services.", "820m", "4 hours (trek) + 1.5 hours (drive)", "Hotel in Pokhara"),
            ]

            for day_num, title, desc, alt, hours, acc in pph_days:
                Itinerary.objects.create(
                    trek=pph, day_number=day_num, title=title, description=desc, altitude=alt, trekking_hours=hours, accommodation=acc, meals_included="Breakfast, Lunch, Dinner"
                )

            # Add included items for PPH
            pph_included = [
                "Kathmandu to Pokhara transportation (Tourist Bus - included)",
                "Pokhara to Nayapul/Nayapul to Pokhara transfer (Private Vehicle/Jeep)",
                "TIMS Card and ACAP (Annapurna Conservation Area Permit)",
                "Experienced, government-licensed, English-speaking trekking guide",
                "Porter service (1 porter for 2 trekkers, maximum weight 20kg)",
                "3 nights accommodation during the trek (best available tea houses/lodges)",
                "3 meals a day (Breakfast, Lunch, Dinner) during the trek",
                "Accommodation in Pokhara (Day 1, 5 - Standard 3-star hotel with breakfast)",
                "Staff costs (insurance, salary, equipment, food, and accommodation for all staff)",
                "Comprehensive first aid kit"
            ]

            for idx, item in enumerate(pph_included, 1):
                IncludedItem.objects.create(trek=pph, item=item, order=idx)

            # Add excluded items for PPH
            pph_excluded = [
                "International airfare to/from Kathmandu",
                "Nepal entry visa fee (obtainable on arrival at TIA)",
                "Domestic flight from Kathmandu to Pokhara (Approx. USD $100-120)",
                "Travel and rescue insurance (mandatory)",
                "Personal expenses (bottled water, soft drinks, alcoholic beverages, phone calls, laundry, Wi-Fi/battery charging)",
                "Showers and hot water charges at tea houses",
                "Tips for guide and porter (expected)",
                "Extra costs due to delays, cancellations, or changes to the itinerary beyond our control (e.g., weather)",
            ]

            for idx, item in enumerate(pph_excluded, 1):
                ExcludedItem.objects.create(trek=pph, item=item, order=idx)

            # Add map coordinates for PPH
            pph_coords = [
                ("Pokhara", Decimal('28.2096'), Decimal('83.9856')),
                ("Nayapul", Decimal('28.3244'), Decimal('83.7744')),
                ("Ghorepani", Decimal('28.3970'), Decimal('83.7020')),
                ("Poon Hill", Decimal('28.3979'), Decimal('83.6974')),
                ("Ghandruk", Decimal('28.3923'), Decimal('83.8440')),
            ]

            for idx, (name, lat, lng) in enumerate(pph_coords, 1):
                MapCoordinate.objects.create(trek=pph, name=name, latitude=lat, longitude=lng, order=idx)
            
            self.stdout.write(self.style.SUCCESS("✅ Poon Hill Trek data loaded."))


            # --- 3. MARDI HIMAL TREK ---
            self.stdout.write("--- Creating Mardi Himal Trek Data ---")
            mht = Trek.objects.create(
                title="Mardi Himal Trek - 8 Days: Close-Up Views of Mount Fishtail",
                slug="mardi-himal-trek-8-days",
                short_description="An off-the-beaten-path experience to the Mardi Himal Base Camp. Enjoy pristine rhododendron forests, authentic Gurung culture, and the closest views of Machhapuchhre (Fishtail) and Annapurna South.",
                long_description="The Mardi Himal Trek is a recently opened trail that is perfect for those seeking solitude and dramatic mountain scenery. The ascent is steady, leading you high up on the ridge for unforgettable views of the Annapurna range and a unique perspective of Machhapuchhre's eastern face.",
                location="Pokhara, Annapurna Region, Himalayas, Nepal",
                start_point="Pokhara",
                latitude=Decimal('28.3810'),
                longitude=Decimal('84.0010'),
                duration_days=8,
                duration_nights=7,
                difficulty="moderate",
                max_altitude=4500,
                max_altitude_feet=14764,
                best_season="spring_autumn",
                price_usd=Decimal('749.00'),
                discount_percentage=0,
                is_featured=True,
                is_popular=True,
                meta_description="Book the 8-Day Mardi Himal Trek from Pokhara. Trek to Mardi Himal Base Camp (4500m) for phenomenal, up-close views of Machhapuchhre.",
                meta_keywords="mardi himal trek, mardi base camp, close up mountain views, machhapuchhre, nepal trekking, pokhara trek",
                image_keywords="Mardi Himal Base Camp, Machhapuchhre close-up, high camp ridge, rhododendron forest, low camp, Siding village, Annapurna panorama"
            )

            # Add itinerary for MHT (Pokhara start/end)
            mht_days = [
                (1, "Arrival in Kathmandu & Transfer to Pokhara", "A transfer to Pokhara via tourist bus (included) or domestic flight (excluded). Hotel check-in and trek briefing in Pokhara.", "820m", "6-8 hours (drive)", "Hotel in Pokhara"),
                (2, "Drive to Phedi & Trek to Forest Camp", "Morning drive from Pokhara to Kande or Phedi. Begin trekking with an easy climb to Australian Camp, followed by a trek through dense forest to Forest Camp (locally known as Kokar).", "2,600m", "5-6 hours", "Tea House"),
                (3, "Trek to Low Camp", "A beautiful trek entirely through rhododendron and maple forest. The path opens up at Low Camp to offer the first great views of Machhapuchhre.", "2,990m", "4-5 hours", "Tea House"),
                (4, "Trek to High Camp", "Trek along the high ridge, offering stunning views of Annapurna South, Hiunchuli, and the Machhapuchhre peak. Reach High Camp.", "3,580m", "4-5 hours", "Tea House"),
                (5, "Hike to Mardi Himal Base Camp & Return to High Camp", "Pre-dawn start to hike up to the Viewpoint (4200m) or Base Camp (4500m) for the sunrise over the massive mountains. Descend back to High Camp.", "4,500m", "5-7 hours", "Tea House"),
                (6, "Trek to Siding Village", "Descend rapidly from the ridge line, taking a different route down to the traditional and less-touristy Gurung village of Siding.", "1,700m", "6-7 hours", "Tea House"),
                (7, "Siding to Lumre & Drive to Pokhara", "A short, easy trek through villages and terraced fields to Lumre/Mardi Pul. Take a local jeep/bus drive from there back to Pokhara.", "820m", "3 hours (trek) + 2 hours (drive)", "Hotel in Pokhara"),
                (8, "Departure from Pokhara", "Final day for travel. Your trekking adventure concludes with a transfer to the bus station or airport for your onward journey.", "820m", "", "Not Included"),
            ]

            for day_num, title, desc, alt, hours, acc in mht_days:
                Itinerary.objects.create(
                    trek=mht, day_number=day_num, title=title, description=desc, altitude=alt, trekking_hours=hours, accommodation=acc, meals_included="Breakfast, Lunch, Dinner"
                )

            # Add included items for MHT
            mht_included = [
                "Kathmandu to Pokhara transportation (Tourist Bus - included)",
                "Pokhara to Phedi/Lumre to Pokhara transfer (Private Vehicle/Jeep)",
                "TIMS Card and ACAP (Annapurna Conservation Area Permit)",
                "Experienced, government-licensed, English-speaking trekking guide",
                "Porter service (1 porter for 2 trekkers, maximum weight 20kg)",
                "5 nights accommodation during the trek (best available tea houses/lodges)",
                "3 meals a day (Breakfast, Lunch, Dinner) during the trek",
                "Accommodation in Pokhara (Day 1, 7 - Standard 3-star hotel with breakfast)",
                "Staff costs (insurance, salary, equipment, food, and accommodation for all staff)",
                "Comprehensive first aid kit"
            ]

            for idx, item in enumerate(mht_included, 1):
                IncludedItem.objects.create(trek=mht, item=item, order=idx)

            # Add excluded items for MHT
            mht_excluded = [
                "International airfare to/from Kathmandu",
                "Nepal entry visa fee (obtainable on arrival at TIA)",
                "Domestic flight from Kathmandu to Pokhara (Approx. USD $100-120)",
                "Travel and rescue insurance (mandatory)",
                "Personal expenses (bottled water, soft drinks, alcoholic beverages, phone calls, laundry, Wi-Fi/battery charging)",
                "Showers and hot water charges at tea houses",
                "Tips for guide and porter (expected)",
                "Extra costs due to delays, cancellations, or changes to the itinerary beyond our control (e.g., weather)",
                "Lunch/Dinner on Day 8 in Pokhara"
            ]

            for idx, item in enumerate(mht_excluded, 1):
                ExcludedItem.objects.create(trek=mht, item=item, order=idx)

            # Add map coordinates for MHT
            mht_coords = [
                ("Pokhara", Decimal('28.2096'), Decimal('83.9856')),
                ("Forest Camp (Kokar)", Decimal('28.3290'), Decimal('83.9702')),
                ("High Camp", Decimal('28.3840'), Decimal('84.0010')),
                ("Mardi Himal Base Camp", Decimal('28.4060'), Decimal('84.0080')),
                ("Siding Village", Decimal('28.3190'), Decimal('83.9880')),
            ]

            for idx, (name, lat, lng) in enumerate(mht_coords, 1):
                MapCoordinate.objects.create(trek=mht, name=name, latitude=lat, longitude=lng, order=idx)
            
            self.stdout.write(self.style.SUCCESS("✅ Mardi Himal Trek data loaded."))


            # --- 4. ANNAPURNA CIRCUIT TREK (SHORT) ---
            self.stdout.write("--- Creating Annapurna Circuit Trek Data (Short) ---")
            act = Trek.objects.create(
                title="Annapurna Circuit Trek (Short) - 15 Days via Thorong La Pass",
                slug="annapurna-circuit-trek-short-15-days",
                short_description="An abridged version of the classic Annapurna Circuit, focusing on the high-altitude route. Cross the formidable Thorong La Pass (5,416m), explore the deepest gorge (Kali Gandaki), and witness incredible geographical and cultural diversity.",
                long_description="The Annapurna Circuit is a world-famous trek that showcases the staggering contrasts of Nepal, from lush rice paddies to arid, high-altitude desert. This itinerary focuses on the core trekking days, taking you over the Thorong La Pass, visiting the holy site of Muktinath, and providing continuous views of the Annapurna and Dhaulagiri massifs.",
                location="Pokhara, Annapurna Region, Himalayas, Nepal",
                start_point="Pokhara",
                latitude=Decimal('28.8475'),
                longitude=Decimal('84.1444'),
                duration_days=15,
                duration_nights=14,
                difficulty="challenging",
                max_altitude=5416,
                max_altitude_feet=17769,
                best_season="spring_autumn",
                price_usd=Decimal('1599.00'),
                discount_percentage=0,
                is_featured=False,
                is_popular=True,
                meta_description="Book the 15-Day Annapurna Circuit Trek from Pokhara. Cross the Thorong La Pass (5416m) and witness the Annapurna and Dhaulagiri ranges. Challenging difficulty.",
                meta_keywords="annapurna circuit trek, thorong la pass, muktinath, annapurna range, high pass trek, nepal trekking, challenging trek",
                image_keywords="Thorong La Pass sign, Manang village, Muktinath Temple, Dhaulagiri view, Gangapurna glacier, Kali Gandaki Gorge, prayer wheels"
            )

            # Add itinerary for ACT (Pokhara start/end)
            act_days = [
                (1, "Arrival in Kathmandu & Transfer to Pokhara", " transfer to Pokhara via tourist bus (included) or domestic flight (excluded). Hotel check-in and trek briefing in Pokhara.", "820m", "6-8 hours (drive)", "Hotel in Pokhara"),
                (2, "Drive from Pokhara to Koto/Jagat", "A long scenic drive by local bus or private jeep to Koto or Jagat, significantly shortening the trek distance and saving time on the lower roads.", "2,600m", "7-9 hours (drive)", "Tea House"),
                (3, "Trek to Chame", "Trek through the Marsyangdi River valley, passing the village of Dharapani. Chame is the headquarters of the Manang district.", "2,710m", "5-6 hours", "Tea House"),
                (4, "Trek to Lower Pisang", "The trail enters the U-shaped Manang Valley. Walk through a steep, narrow valley, often crossing the river. Enjoy the first clear views of Annapurna II and IV.", "3,250m", "5-6 hours", "Tea House"),
                (5, "Trek to Manang (Upper Route)", "Take the upper route via Ghyaru/Ngawal for spectacular views and better acclimatization. Manang is a large, historically significant village.", "3,540m", "6-7 hours", "Tea House"),
                (6, "Acclimatization Day in Manang", "A rest day to help with altitude. Suggested side trips include Gangapurna Lake or the view point above the village. Attend a talk on altitude sickness.", "3,540m", "2-3 hours (hike)", "Tea House"),
                (7, "Trek to Yak Kharka", "Continue the gradual climb through the Marsyangdi valley. The landscape becomes more arid and alpine as you gain altitude.", "4,050m", "3-4 hours", "Tea House"),
                (8, "Trek to Thorong Phedi", "A short but challenging day, passing through the village of Ledar. Climb to the base of the pass at Thorong Phedi (or High Camp, depending on conditions).", "4,450m", "3-4 hours", "Tea House"),
                (9, "Cross Thorong La Pass (5,416m) to Muktinath", "The most demanding day: a pre-dawn start to cross the Thorong La Pass, the highest point of the trek. A long descent to the sacred pilgrimage site of Muktinath.", "3,760m", "8-10 hours", "Tea House"),
                (10, "Trek/Drive to Jomsom & Flight to Pokhara", "Visit the Muktinath Temple complex. Trek down to Jomsom or take a short drive (to save time). Fly from Jomsom to Pokhara in the afternoon. End of trek.", "820m", "20 minutes (flight)", "Hotel in Pokhara"),
                (11, "Free Day in Pokhara", "A leisure day in Pokhara to recover, explore the city, or do optional activities like boating on Fewa Lake or paragliding.", "820m", "N/A", "Hotel in Pokhara"),
                (12, "Pokhara to Kathmandu", "Transfer from Pokhara to Kathmandu via tourist bus (included) or domestic flight (excluded). Hotel check-in in Kathmandu.", "1,400m", "6-8 hours (drive)", "Hotel in Kathmandu"),
                (13, "Sightseeing Day in Kathmandu Valley", "Guided sightseeing tour of UNESCO World Heritage Sites: Swayambhunath (Monkey Temple), Pashupatinath, and Boudhanath Stupa.", "1,400m", "5-6 hours", "Hotel in Kathmandu"),
                (14, "Departure from Kathmandu", "Transfer to Tribhuvan International Airport (TIA) for your final departure.", "1,400m", "", "Not Included"),
            ]

            for day_num, title, desc, alt, hours, acc in act_days:
                Itinerary.objects.create(
                    trek=act, day_number=day_num, title=title, description=desc, altitude=alt, trekking_hours=hours, accommodation=acc, meals_included="Breakfast, Lunch, Dinner"
                )

            # Add included items for ACT
            act_included = [
                "Kathmandu to Pokhara/Pokhara to Kathmandu transportation (Tourist Bus - included)",
                "Pokhara to Koto/Jagat drive (Jeep/Bus)",
                "Domestic Flight Jomsom to Pokhara",
                "TIMS Card and ACAP (Annapurna Conservation Area Permit)",
                "Experienced, government-licensed, English-speaking trekking guide",
                "Porter service (1 porter for 2 trekkers, maximum weight 20kg)",
                "11 nights accommodation during the trek (best available tea houses/lodges)",
                "3 meals a day (Breakfast, Lunch, Dinner) during the trek",
                "Accommodation in Pokhara (Day 1, 10, 11 - Standard 3-star hotel with breakfast)",
                "Accommodation in Kathmandu (Day 12, 13 - Standard 3-star hotel with breakfast)",
                "Staff costs (insurance, salary, equipment, food, and accommodation for all staff)",
                "Comprehensive first aid kit",
                "Company T-shirt, trekking map, and certificate of completion",
                "Farewell dinner in Pokhara"
            ]

            for idx, item in enumerate(act_included, 1):
                IncludedItem.objects.create(trek=act, item=item, order=idx)

            # Add excluded items for ACT
            act_excluded = [
                "International airfare to/from Kathmandu",
                "Nepal entry visa fee (obtainable on arrival at TIA)",
                "Domestic flight from Kathmandu to Pokhara (Approx. USD $100-120)",
                "Travel and rescue insurance (mandatory and must cover high altitude rescue)",
                "Personal expenses (bottled water, soft drinks, alcoholic beverages, phone calls, laundry, Wi-Fi/battery charging)",
                "Showers and hot water charges at tea houses",
                "Tips for guide and porter (expected)",
                "Extra costs due to delays, cancellations, or changes to the itinerary beyond our control (e.g., Jomsom flight cancellation)",
                "Lunch/Dinner in Kathmandu and Pokhara (except farewell dinner)"
            ]

            for idx, item in enumerate(act_excluded, 1):
                ExcludedItem.objects.create(trek=act, item=item, order=idx)

            # Add map coordinates for ACT
            act_coords = [
                ("Pokhara", Decimal('28.2096'), Decimal('83.9856')),
                ("Chame", Decimal('28.5445'), Decimal('84.2255')),
                ("Manang", Decimal('28.6738'), Decimal('84.0252')),
                ("Thorong Phedi", Decimal('28.7758'), Decimal('83.9610')),
                ("Thorong La Pass", Decimal('28.8475'), Decimal('84.1444')),
                ("Muktinath", Decimal('28.8149'), Decimal('83.8767')),
                ("Jomsom", Decimal('28.7766'), Decimal('83.7441')),
            ]

            for idx, (name, lat, lng) in enumerate(act_coords, 1):
                MapCoordinate.objects.create(trek=act, name=name, latitude=lat, longitude=lng, order=idx)
            
            self.stdout.write(self.style.SUCCESS("✅ Annapurna Circuit Trek (Short) data loaded."))


            # --- 5. EVEREST BASE CAMP TREK (EBC) - 14 DAYS ---
            self.stdout.write("--- Creating EBC Trek Data ---")
            ebc_new = Trek.objects.create(
                title="Everest Base Camp Trek - 14 Days Journey to the World's Highest Peak",
                slug="everest-base-camp-trek-14-days",
                short_description="Experience the legendary Everest Base Camp trek, walking in the footsteps of mountaineering legends through Sherpa villages, ancient monasteries, and breathtaking Himalayan landscapes to reach the base of Mount Everest.",
                long_description="The Everest Base Camp trek is one of the most iconic treks in the world. Journey through the stunning Khumbu region, passing through traditional Sherpa villages, ancient Buddhist monasteries, and breathtaking mountain landscapes. Stand at the base of the world's highest mountain and experience the magnificent Himalayan culture.",
                location="Pokhara, Kathmandu, Everest Region, Himalayas, Nepal",
                start_point="Pokhara",
                latitude=Decimal('28.0026'),
                longitude=Decimal('86.8528'),
                duration_days=14,
                duration_nights=13,
                difficulty="moderate_challenging",
                max_altitude=5545, # Kala Patthar
                max_altitude_feet=18192,
                best_season="spring_autumn",
                price_usd=Decimal('1599.00'),
                discount_percentage=0,
                is_featured=True,
                is_popular=True,
                meta_description="Join our 14-day Everest Base Camp trek. Experience Sherpa culture, stunning Himalayan views, and reach the base of Mount Everest. Book now!",
                meta_keywords="everest base camp trek, EBC trek, everest trekking, nepal trekking, himalayan trek, sherpa villages, khumbu region, mount everest",
                image_keywords="Everest Base Camp, Kala Patthar sunrise, Namche Bazaar, Tengboche Monastery, Sherpa villages, Dudh Koshi River, prayer flags, Himalayan peaks, Khumbu region"
            )

            # Add itinerary for EBC (Pokhara start/end)
            ebc_new_days = [
                (1, "Arrival in Kathmandu", "Reach Kathmandu and settle in", "1400m", "0 hours", "Hotel in Kathmandu"),
                (2, "Final gear check and preparation for the morning flight", "Prepare gear and rest", "1400m", "0 hours", "Hotel in Kathmandu"),
                (3, "Fly to Lukla (2,860m), Trek to Phakding", "Early morning flight from Kathmandu to Tenzing-Hillary Airport at Lukla. Begin trekking along the Dudh Koshi River to Phakding.", "2,610m", "3-4 hours", "Tea House"),
                (4, "Trek to Namche Bazaar (3,440m)", "Cross multiple suspension bridges. Enter Sagarmatha National Park. Steep climb up to the Sherpa capital of Namche Bazaar.", "3,440m", "5-6 hours", "Tea House"),
                (5, "Acclimatization Day in Namche", "Rest day to help with altitude. Morning hike to the Everest View Hotel for the first clear views of Mt. Everest, Lhotse, and Ama Dablam.", "3,440m", "2-3 hours (hike)", "Tea House"),
                (6, "Trek to Tengboche", "Climb to the famous Tengboche Monastery (3,860m), offering spectacular panoramic views of Everest, Lhotse, and Ama Dablam.", "3,860m", "5-6 hours", "Tea House"),
                (7, "Trek to Dingboche", "Descend through a forest and cross the Imja Khola, then climb steadily to the village of Dingboche, situated in the Imja Valley.", "4,410m", "5-6 hours", "Tea House"),
                (8, "Acclimatization Day in Dingboche", "Rest day with a recommended hike to Nagarjuna Hill or Chhukung Valley for panoramic views and better acclimatization.", "4,410m", "3-4 hours (hike)", "Tea House"),
                (9, "Trek to Lobuche", "Trek up the Khumbu Khola Valley, passing the Everest Memorial (Dugla Pass) where monuments honor lost mountaineers.", "4,910m", "5-6 hours", "Tea House"),
                (10, "Trek to Gorak Shep & Everest Base Camp (EBC)", "Morning trek to Gorak Shep (5140m). After lunch, hike to Everest Base Camp (5364m). Return to Gorak Shep for the night.", "5,140m", "7-8 hours", "Tea House"),
                (11, "Hike to Kala Patthar (5,545m) & Trek to Pheriche", "Pre-dawn hike to Kala Patthar (5545m) for sunrise views of Everest. Return to Gorak Shep for breakfast and descend to Pheriche.", "4,371m", "7-8 hours", "Tea House"),
                (12, "Trek to Namche Bazaar", "A long descent, retracing the path, passing through Pangboche and Tengboche, and arriving at Namche Bazaar.", "3,440m", "6-7 hours", "Tea House"),
                (13, "Trek to Lukla", "Final day of trekking, descending steeply to Phakding and continuing back to Lukla.", "2,860m", "6-7 hours", "Tea House"),
                (14, "Fly to Kathmandu", "Early morning flight from Lukla back to Kathmandu. Transfer to hotel for rest/leisure.", "1,400m", "35 minutes (flight)", "Hotel in Kathmandu"),
            ]

            for day_num, title, desc, alt, hours, acc in ebc_new_days:
                Itinerary.objects.create(
                    trek=ebc_new, day_number=day_num, title=title, description=desc, altitude=alt, trekking_hours=hours, accommodation=acc, meals_included="Breakfast, Lunch, Dinner"
                )
            
            # (EBC Included/Excluded/Map items go here)
            self.stdout.write(self.style.SUCCESS("✅ EBC Trek data loaded."))
            

            # --- 6. MANASLU CIRCUIT TREK (MCT) ---
            self.stdout.write("--- Creating Manaslu Circuit Trek Data ---")
            mct = Trek.objects.create(
                title="Manaslu Circuit Trek - 15 Days via Larkya La Pass",
                slug="manaslu-circuit-trek-15-days",
                short_description="A culturally and geographically spectacular restricted area trek circumnavigating the world's eighth-highest mountain, Manaslu. Cross the challenging Larkya La Pass (5,106m) and explore pristine Tibetan-Buddhist and Gurung villages.",
                long_description="The Manaslu Circuit is one of Nepal's finest treks, offering stunning views, diverse scenery, and deep cultural immersion due to its proximity to Tibet. The route follows the ancient salt-trading path and is a fully-supported tea house trek that provides an authentic, off-the-beaten-path experience.",
                location="Pokhara, Kathmandu, Manaslu Region, Himalayas, Nepal",
                start_point="Pokhara",
                latitude=Decimal('28.6946'),
                longitude=Decimal('84.4530'),
                duration_days=15,
                duration_nights=14,
                difficulty="challenging",
                max_altitude=5106,
                max_altitude_feet=16752,
                best_season="spring_autumn",
                price_usd=Decimal('1899.00'),
                discount_percentage=0,
                is_featured=True,
                is_popular=False, # Often less popular than ABC/EBC but highly ranked
                meta_description="Book the 15-Day Manaslu Circuit Trek. Cross Larkya La Pass (5,106m) and trek around Manaslu. Restricted Area Permit required. Challenging difficulty.",
                meta_keywords="manaslu circuit trek, larkya la pass, manaslu region, restricted area trek, nepal trekking, tibetan culture",
                image_keywords="Manaslu view, Larkya La Pass, Gurung village, Budi Gandaki river, Kani gate, prayer wheels, Tibetan Mani walls"
            )

            # Add itinerary for MCT (Pokhara start/end)
            mct_days = [
                (1, "Arrival in Kathmandu", "Reach Kathmandu and settle in. Prepare for the morning drive. (Note: Start point in core data is Pokhara, so this day assumes arrival in Kathmandu first).", "1400m", "0 hours", "Hotel in Kathmandu"),
                (2, "Drive Kathmandu to Soti Khola", "A long, scenic drive from Kathmandu to Soti Khola, the starting point of the trek. Drive along the Trisuli and Budi Gandaki river valleys.", "710m", "7-9 hours (drive)", "Tea House"),
                (3, "Trek to Machha Khola", "Follow the Budi Gandaki River, traversing rice paddies, Gurung villages, and forests. The trail involves uphill and downhill sections.", "900m", "6-7 hours", "Tea House"),
                (4, "Trek to Jagat", "Trek through a narrow gorge and ascend to the hot springs at Tatopani. Cross the river and continue to Jagat, the entry point of the restricted area.", "1,340m", "6-7 hours", "Tea House"),
                (5, "Trek to Deng", "The trail enters the restricted area. Pass through several small villages, forests, and across the river, arriving at Deng.", "1,860m", "6-7 hours", "Tea House"),
                (6, "Trek to Namrung", "Trek through rhododendron forests. The culture becomes distinctly Tibetan as you enter the upper Nupri region. Pass through impressive Mani walls and Kani gates.", "2,630m", "6-7 hours", "Tea House"),
                (7, "Trek to Samagaun", "The views of Manaslu and Himalchuli become increasingly spectacular. Pass through Lho and Shyala, where you see the monastery and prayer flags, before reaching Samagaun.", "3,530m", "6-7 hours", "Tea House"),
                (8, "Acclimatization Day in Samagaun", "Rest day. Hike to Pungyen Gompa (3,870m) or Manaslu Base Camp (4,400m) for phenomenal close-up views and better acclimatization.", "3,530m", "4-5 hours (hike)", "Tea House"),
                (9, "Trek to Samdo", "A short day, continuing along the Budi Gandaki River. The landscape becomes more arid and mountainous. Arrive at the remote village of Samdo, near the Tibet border.", "3,860m", "3-4 hours", "Tea House"),
                (10, "Trek to Dharmasala/Larkya Phedi", "A gentle ascent to the stone shelter at Dharmasala, also known as Larkya Phedi. An early stop is made to prepare for the pass crossing the next day.", "4,460m", "4-5 hours", "Tea House"),
                (11, "Cross Larkya La Pass (5,106m) to Bimthang", "The most challenging day: pre-dawn start to ascend the pass. Enjoy incredible views of Himlung, Cheo Himal, Kangguru, and Annapurna II. A long descent to Bimthang.", "3,720m", "8-10 hours", "Tea House"),
                (12, "Trek to Tilije", "A beautiful, easy descent through rhododendron and pine forest, following the Dudh Khola (Milk River) to the Gurung village of Tilije.", "2,300m", "5-6 hours", "Tea House"),
                (13, "Trek to Dharapani & Drive to Besisahar", "Trek through the Marsyangdi River valley. The trail joins the Annapurna Circuit at Dharapani. Take a local jeep drive down to Besisahar.", "760m", "2 hours (trek) + 5 hours (drive)", "Tea House"),
                (14, "Drive from Besisahar to Pokhara", "Morning drive from Besisahar directly back to Pokhara.", "820m", "4-5 hours (drive)", "Hotel in Pokhara"),
                (15, "Departure from Pokhara", "Final day for travel. Your trekking adventure concludes with a transfer to the bus station or airport for your onward journey.", "820m", "", "Not Included"),
            ]

            for day_num, title, desc, alt, hours, acc in mct_days:
                Itinerary.objects.create(
                    trek=mct, day_number=day_num, title=title, description=desc, altitude=alt, trekking_hours=hours, accommodation=acc, meals_included="Breakfast, Lunch, Dinner"
                )

            # Add included items for MCT
            mct_included = [
                "Kathmandu to Pokhara transportation (Tourist Bus - included)",
                "Domestic flight from Kathmandu to Pokhara (Approx. USD $100-120) on Day 1 (Bus included)",
                "Drive Kathmandu to Soti Khola (Day 2 - Private Jeep/Bus) and Besisahar to Pokhara (Day 14 - Private Jeep/Bus)",
                "Manaslu Restricted Area Permit (MRAP), ACAP, and Annapurna Conservation Area Permit (ACAP)",
                "Experienced, government-licensed, English-speaking trekking guide (mandatory for restricted areas)",
                "Porter service (1 porter for 2 trekkers, maximum weight 20kg)",
                "12 nights accommodation during the trek (best available tea houses/lodges)",
                "Accommodation in Kathmandu (Day 1, 13 - Standard 3-star hotel with breakfast)",
                "Accommodation in Pokhara (Day 14 - Standard 3-star hotel with breakfast)",
                "3 meals a day (Breakfast, Lunch, Dinner) during the trek",
                "Staff costs (insurance, salary, equipment, food, and accommodation for all staff)",
                "Comprehensive first aid kit, sleeping bag and down jacket (if needed, return after trek)",
                "Farewell dinner in Pokhara"
            ]

            for idx, item in enumerate(mct_included, 1):
                IncludedItem.objects.create(trek=mct, item=item, order=idx)

            # Add excluded items for MCT
            mct_excluded = [
                "International airfare to/from Kathmandu",
                "Nepal entry visa fee (obtainable on arrival at TIA)",
                "Domestic flight from Kathmandu to Pokhara (Approx. USD $100-120) on Day 1 or 14 (Bus included)",
                "Travel and rescue insurance (mandatory and must cover high altitude rescue)",
                "Personal expenses (bottled water, soft drinks, alcoholic beverages, phone calls, laundry, Wi-Fi/battery charging, hot showers)",
                "Tips for guide and porter (expected)",
                "Extra costs due to delays, cancellations, or changes to the itinerary beyond our control (e.g., weather)",
                "Lunch/Dinner on Day 15 in Pokhara"
            ]

            for idx, item in enumerate(mct_excluded, 1):
                ExcludedItem.objects.create(trek=mct, item=item, order=idx)

            # Add map coordinates for MCT
            mct_coords = [
                ("Kathmandu", Decimal('27.7172'), Decimal('85.3240')),
                ("Soti Khola", Decimal('28.3242'), Decimal('84.7082')),
                ("Jagat", Decimal('28.4682'), Decimal('84.7226')),
                ("Samagaun", Decimal('28.6738'), Decimal('84.0252')),
                ("Larkya Phedi", Decimal('28.6775'), Decimal('84.4530')),
                ("Larkya La Pass", Decimal('28.6946'), Decimal('84.4530')),
                ("Bimthang", Decimal('28.6015'), Decimal('84.5502')),
                ("Besisahar", Decimal('28.2323'), Decimal('84.3854')),
                ("Pokhara", Decimal('28.2096'), Decimal('83.9856')),
            ]

            for idx, (name, lat, lng) in enumerate(mct_coords, 1):
                MapCoordinate.objects.create(trek=mct, name=name, latitude=lat, longitude=lng, order=idx)
            
            self.stdout.write(self.style.SUCCESS("✅ Manaslu Circuit Trek Data loaded."))


            # --- 7. LANGTANG VALLEY TREK (LVT) ---
            self.stdout.write("--- Creating Langtang Valley Trek Data ---")
            lvt = Trek.objects.create(
                title="Langtang Valley Trek - 10 Days: Valley of Glaciers",
                slug="langtang-valley-trek-10-days",
                short_description="Explore the beautiful Langtang Valley, known as the 'Valley of Glaciers'. Trek through deep forests, experience traditional Tamang culture, and enjoy stunning, close-up views of the Langtang Lirung range, all close to the Tibetan border.",
                long_description="A perfect moderate trek famous for its accessibility from Kathmandu and the resilience of the local Tamang communities. The trek combines spectacular alpine scenery, including Langtang Lirung (7,227m), with lush forests and deep cultural immersion. The optional ascent of Tserko Ri provides unparalleled panoramic views.",
                location="Pokhara, Kathmandu, Langtang Region, Himalayas, Nepal",
                start_point="Pokhara",
                latitude=Decimal('28.2185'),
                longitude=Decimal('85.5684'),
                duration_days=10,
                duration_nights=9,
                difficulty="moderate",
                max_altitude=5033,  # Tserko Ri
                max_altitude_feet=16512,
                best_season="spring_autumn",
                price_usd=Decimal('899.00'),
                discount_percentage=0,
                is_featured=False,
                is_popular=True,
                meta_description="Book the 10-Day Langtang Valley Trek from Pokhara. Explore Kyanjin Gompa and ascend Tserko Ri (5033m) for panoramic views. Moderate difficulty.",
                meta_keywords="langtang valley trek, langtang lirung, tserko ri, kyanjin gompa, tamang culture, nepal trekking, moderate trek",
                image_keywords="Langtang Lirung view, Tamang village, Rhododendron forest, Kyanjin Gompa, prayer wheels, Tserko Ri, Syabrubesi"
            )

            # Add itinerary for LVT (Pokhara start/end)
            lvt_days = [
                (1, "Arrival in Kathmandu", "Reach Kathmandu and settle in.", "1400m", "0 hours", "Hotel in Kathmandu"),
                (2, "Final gear check and preparation (Kathmandu)", "Prepare gear and rest. Attend trek briefing. (Note: The trek technically begins near Kathmandu, not Pokhara.)", "1400m", "6-8 hours (drive)", "Hotel in Kathmandu"),
                (3, "Drive Kathmandu to Syabrubesi", "A long, scenic drive via local bus or private jeep to Syabrubesi, the starting point of the trek. Drive through mountain roads and small villages.", "1,460m", "7-9 hours (drive)", "Tea House"),
                (4, "Trek to Lama Hotel", "The trek begins, following the Langtang Khola (river). Pass through dense rhododendron, oak, and bamboo forests. Keep an eye out for Red Pandas.", "2,470m", "6-7 hours", "Tea House"),
                (5, "Trek to Mundu (near Langtang Village)", "Continue ascending through the gorge. The valley gradually opens up. Pass the rebuilt Langtang village and settle in Mundu.", "3,550m", "5-6 hours", "Tea House"),
                (6, "Trek to Kyanjin Gompa", "A shorter, highly scenic walk through yak pastures and traditional mani walls to Kyanjin Gompa, the highest settlement in the valley.", "3,870m", "3-4 hours", "Tea House"),
                (7, "Exploration Day & Tserko Ri Hike", "Acclimatization day. Early morning hike up **Tserko Ri (5,033m)** or Kyanjin Ri for breathtaking 360-degree views of the Langtang range, including Shishapangma (in Tibet).", "5,033m", "6-7 hours (hike)", "Tea House"),
                (8, "Kyanjin Gompa to Lama Hotel", "A long day of easy descent, quickly losing altitude as you retrace your steps through the valley and forest.", "2,470m", "6-7 hours", "Tea House"),
                (9, "Lama Hotel to Syabrubesi & Drive to Kathmandu", "The final leg of the trek. Drive from Syabrubesi back to Kathmandu. Celebrate the end of the trek.", "1,400m", "3 hours (trek) + 7-9 hours (drive)", "Hotel in Kathmandu"),
                (10, "Departure from Kathmandu via Pokhara Transfer", "Transfer from Kathmandu to Pokhara via tourist bus (included) or domestic flight (excluded). Final departure or onward journey from Pokhara.", "820m", "6-8 hours (travel)", "Not Included"),
            ]

            for day_num, title, desc, alt, hours, acc in lvt_days:
                Itinerary.objects.create(
                    trek=lvt, day_number=day_num, title=title, description=desc, altitude=alt, trekking_hours=hours, accommodation=acc, meals_included="Breakfast, Lunch, Dinner"
                )

            # Add included items for LVT
            lvt_included = [
                "Kathmandu to Pokhara/Pokhara to Kathmandu transportation (Tourist Bus - included)",
                "Drive Kathmandu to Syabrubesi and return (Private Jeep/Bus)",
                "Langtang National Park Entry Permit and TIMS Card",
                "Experienced, government-licensed, English-speaking trekking guide",
                "Porter service (1 porter for 2 trekkers, maximum weight 20kg)",
                "6 nights accommodation during the trek (best available tea houses/lodges)",
                "Accommodation in Kathmandu (Day 1, 2, 9 - Standard 3-star hotel with breakfast)",
                "3 meals a day (Breakfast, Lunch, Dinner) during the trek",
                "Staff costs (insurance, salary, equipment, food, and accommodation for all staff)",
                "Comprehensive first aid kit",
                "Farewell dinner in Kathmandu"
            ]

            for idx, item in enumerate(lvt_included, 1):
                IncludedItem.objects.create(trek=lvt, item=item, order=idx)

            # Add excluded items for LVT
            lvt_excluded = [
                "International airfare to/from Kathmandu",
                "Nepal entry visa fee (obtainable on arrival at TIA)",
                "Domestic flight from Kathmandu to Pokhara (Approx. USD $100-120) on Day 1 or 10 (Bus included)",
                "Travel and rescue insurance (mandatory)",
                "Personal expenses (bottled water, soft drinks, alcoholic beverages, phone calls, laundry, Wi-Fi/battery charging, hot showers)",
                "Tips for guide and porter (expected)",
                "Extra costs due to road/weather delays, cancellations, or changes to the itinerary beyond our control",
                "Lunch/Dinner on Day 1, 2, 9 (except farewell dinner)"
            ]

            for idx, item in enumerate(lvt_excluded, 1):
                ExcludedItem.objects.create(trek=lvt, item=item, order=idx)

            # Add map coordinates for LVT
            lvt_coords = [
                ("Kathmandu", Decimal('27.7172'), Decimal('85.3240')),
                ("Syabrubesi", Decimal('28.1670'), Decimal('85.3470')),
                ("Lama Hotel", Decimal('28.2576'), Decimal('85.4216')),
                ("Langtang Village", Decimal('28.3262'), Decimal('85.5584')),
                ("Kyanjin Gompa", Decimal('28.2185'), Decimal('85.5684')),
                ("Tserko Ri (Viewpoint)", Decimal('28.2255'), Decimal('85.5905')),
                ("Pokhara", Decimal('28.2096'), Decimal('83.9856')),
            ]

            for idx, (name, lat, lng) in enumerate(lvt_coords, 1):
                MapCoordinate.objects.create(trek=lvt, name=name, latitude=lat, longitude=lng, order=idx)
            
            self.stdout.write(self.style.SUCCESS("✅ Langtang Valley Trek Data loaded."))


            # --- 8. UPPER MUSTANG TREK (UMT) ---
            self.stdout.write("--- Creating Upper Mustang Trek Data ---")
            umt = Trek.objects.create(
                title="Upper Mustang Trek - 17 Days: Ancient Forbidden Kingdom of Lo",
                slug="upper-mustang-trek-17-days",
                short_description="An incredible journey into the restricted, trans-Himalayan kingdom of Lo. Explore the walled city of Lo Manthang, ancient monasteries, and arid Tibetan-like landscapes. This is a unique cultural experience in a rain-shadow region.",
                long_description="Upper Mustang, or the Kingdom of Lo, offers a glimpse into a world untouched by modern changes. Located high in the rain shadow of the Annapurna and Dhaulagiri ranges, its arid, colorful landscapes, deep canyons, and Tibetan-Buddhist culture make it one of the most sought-after trekking destinations. A special permit is mandatory.",
                location="Pokhara, Mustang, Lo Manthang, Himalayas, Nepal",
                start_point="Pokhara",
                latitude=Decimal('29.1866'),
                longitude=Decimal('83.9780'),
                duration_days=17,
                duration_nights=16,
                difficulty="moderate_challenging",
                max_altitude=3950,
                max_altitude_feet=12959,
                best_season="spring_autumn_monsoon", # Best even in Monsoon
                price_usd=Decimal('2899.00'),
                discount_percentage=0,
                is_featured=True,
                is_popular=False,
                meta_description="Book the 17-Day Upper Mustang Trek from Pokhara. Visit the ancient walled city of Lo Manthang. Special Permit Required. Best during the monsoon.",
                meta_keywords="upper mustang trek, lo manthang, forbidden kingdom, restricted area nepal, tibetan culture, jomsom, annapurna region",
                image_keywords="Lo Manthang wall, arid landscape, ancient monastery, cave dwellings, Mustang King, Tiji festival, Kali Gandaki River"
            )

            # Add itinerary for UMT (Pokhara start/end)
            umt_days = [
                (1, "Arrival in Kathmandu & Transfer to Pokhara", "Airport pickup at TIA, followed by transfer to Pokhara via tourist bus (included) or domestic flight (excluded). Hotel check-in and final permit preparation in Pokhara.", "820m", "6-8 hours (drive)", "Hotel in Pokhara"),
                (2, "Fly Pokhara to Jomsom & Trek to Kagbeni", "Early morning scenic flight to Jomsom (the entry point to Mustang). Meet the support staff. Trek along the Kali Gandaki river to the village of Kagbeni.", "2,810m", "3-4 hours", "Tea House"),
                (3, "Trek to Chele (Restricted Area Entry)", "The journey enters the restricted area. The trail follows the river bank, crossing the river near Tangbe. Trek into a rugged landscape to Chele.", "3,050m", "5-6 hours", "Tea House"),
                (4, "Trek to Geling", "Climb the Chele La pass (3,620m) with great views of the Kali Gandaki valley. Pass through Samar and cross several ridges and small passes before descending to Geling.", "3,570m", "6-7 hours", "Tea House"),
                (5, "Trek to Charang", "Hike past the Nyi La pass (4,020m) and Ghami (where you see a long mani wall). Cross the river and climb a ridge to the large village of Charang.", "3,560m", "5-6 hours", "Tea House"),
                (6, "Trek to Lo Manthang (Walled City)", "Visit the Charang Gompa and Chorten before starting the trek. Climb the Lo La pass (3,950m) and get your first view of the walled city, Lo Manthang. Descend into the city.", "3,840m", "4-5 hours", "Tea House/Guesthouse"),
                (7, "Exploration Day in Lo Manthang", "Explore the walled city, including the palace, the ancient Thugchen Gompa, and Jampa Gompa. Optional pony ride or jeep trip to the unique Sky Caves near Chhosar.", "3,840m", "N/A", "Tea House/Guesthouse"),
                (8, "Lo Manthang to Ghami", "Begin the journey south, returning via a slightly different route for new views. Trek over a pass and descend to the village of Ghami.", "3,520m", "6-7 hours", "Tea House"),
                (9, "Trek to Samar", "Continue the descent, crossing the Nyi La pass again and descending back toward the village of Samar.", "3,660m", "6-7 hours", "Tea House"),
                (10, "Trek to Chhusang", "Trek back toward the Kali Gandaki River. Pass through a unique canyon section before arriving at Chhusang.", "2,980m", "6-7 hours", "Tea House"),
                (11, "Trek to Muktinath (Non-Mustang)", "Leave the restricted area and trek towards Muktinath. Visit the famous Hindu/Buddhist pilgrimage temple complex.", "3,760m", "5-6 hours", "Tea House"),
                (12, "Trek to Jomsom", "A gentle descent along the river valley to Jomsom, the district headquarters. Prepare for the morning flight.", "2,720m", "5-6 hours", "Tea House"),
                (13, "Fly Jomsom to Pokhara", "Early morning scenic flight from Jomsom to Pokhara. Transfer to hotel. Afternoon free for rest and exploration.", "820m", "20 mins (flight)", "Hotel in Pokhara"),
                (14, "Free Day in Pokhara", "A buffer day for any potential flight delays from Jomsom or for rest/sightseeing.", "820m", "N/A", "Hotel in Pokhara"),
                (15, "Pokhara to Kathmandu", "Transfer from Pokhara to Kathmandu via tourist bus (included) or domestic flight (excluded). Hotel check-in in Kathmandu.", "1,400m", "6-8 hours (drive)", "Hotel in Kathmandu"),
                (16, "Sightseeing Day in Kathmandu Valley", "Guided sightseeing tour of UNESCO World Heritage Sites: Boudhanath Stupa, Pashupatinath Temple, or other key sites.", "1,400m", "5-6 hours", "Hotel in Kathmandu"),
                (17, "Departure from Kathmandu via Pokhara Transfer", "Transfer from Kathmandu to Pokhara via tourist bus (included) or domestic flight (excluded). Final departure or onward journey from Pokhara.", "820m", "6-8 hours (travel)", "Not Included"),
            ]

            for day_num, title, desc, alt, hours, acc in umt_days:
                Itinerary.objects.create(
                    trek=umt, day_number=day_num, title=title, description=desc, altitude=alt, trekking_hours=hours, accommodation=acc, meals_included="Breakfast, Lunch, Dinner"
                )

            # Add included items for UMT
            umt_included = [
                "Kathmandu to Pokhara/Pokhara to Kathmandu transportation (Tourist Bus - included)",
                "Domestic Flights: Pokhara to Jomsom and Jomsom to Pokhara",
                "Upper Mustang Special Trekking Permit (USD $500 per person for the first 10 days) and ACAP",
                "Experienced, government-licensed, English-speaking trekking guide (mandatory)",
                "Porter service (1 porter for 2 trekkers, maximum weight 20kg)",
                "11 nights accommodation during the trek (best available tea houses/lodges)",
                "Accommodation in Pokhara (Day 1, 13, 14 - Standard 3-star hotel with breakfast)",
                "Accommodation in Kathmandu (Day 15, 16 - Standard 3-star hotel with breakfast)",
                "3 meals a day (Breakfast, Lunch, Dinner) during the trek",
                "Staff costs (insurance, salary, equipment, food, and accommodation for all staff)",
                "Comprehensive first aid kit",
                "Farewell dinner in Kathmandu"
            ]

            for idx, item in enumerate(umt_included, 1):
                IncludedItem.objects.create(trek=umt, item=item, order=idx)

            # Add excluded items for UMT
            umt_excluded = [
                "International airfare to/from Kathmandu",
                "Nepal entry visa fee (obtainable on arrival at TIA)",
                "Domestic flight from Kathmandu to Pokhara (Approx. USD $100-120) on Day 1 or 17 (Bus included)",
                "Travel and rescue insurance (mandatory and must cover helicopter evacuation)",
                "Personal expenses (bottled water, soft drinks, alcoholic beverages, phone calls, laundry, Wi-Fi/battery charging, hot showers)",
                "Tips for guide and porter (expected)",
                "Extra costs due to delays, cancellations, or changes to the itinerary beyond our control (e.g., Jomsom flight cancellation)",
                "Lunch/Dinner in Kathmandu and Pokhara (except farewell dinner)"
            ]

            for idx, item in enumerate(umt_excluded, 1):
                ExcludedItem.objects.create(trek=umt, item=item, order=idx)

            # Add map coordinates for UMT
            umt_coords = [
                ("Pokhara", Decimal('28.2096'), Decimal('83.9856')),
                ("Jomsom", Decimal('28.7766'), Decimal('83.7441')),
                ("Kagbeni", Decimal('28.8149'), Decimal('83.7679')),
                ("Chele", Decimal('28.8953'), Decimal('83.8055')),
                ("Geling", Decimal('29.0062'), Decimal('83.9452')),
                ("Charang", Decimal('29.0550'), Decimal('84.0040')),
                ("Lo Manthang", Decimal('29.1866'), Decimal('83.9780')),
                ("Muktinath", Decimal('28.8149'), Decimal('83.8767')),
                ("Kathmandu", Decimal('27.7172'), Decimal('85.3240')),
            ]

            for idx, (name, lat, lng) in enumerate(umt_coords, 1):
                MapCoordinate.objects.create(trek=umt, name=name, latitude=lat, longitude=lng, order=idx)
            
            self.stdout.write(self.style.SUCCESS("✅ Upper Mustang Trek Data loaded."))


            # --- 9. RARA LAKE TREK (RLT) ---
            self.stdout.write("--- Creating Rara Lake Trek Data ---")
            rlt = Trek.objects.create(
                title="Rara Lake Trek - 15 Days: Wilderness Trek to Nepal's Largest Lake",
                slug="rara-lake-trek-15-days-flying-route",
                short_description="Journey to Rara Lake, Nepal's largest lake, nestled within Rara National Park in remote far-western Nepal. This trek offers a true wilderness experience, solitude, and stunning views of the crystal-clear 'Queen of Lakes.'",
                long_description="The Rara Lake trek takes you deep into the isolated Mugu region. It is a challenging, off-the-beaten-path adventure involving multiple domestic flights and a camping-style experience (basic accommodation is available). The reward is the majestic, changing colors of Rara Lake and the serenity of the national park.",
                location="Pokhara, Kathmandu, Mugu, Rara National Park, Nepal",
                start_point="Pokhara",
                latitude=Decimal('29.5085'),
                longitude=Decimal('82.9090'),
                duration_days=15,
                duration_nights=14,
                difficulty="moderate_challenging",
                max_altitude=3180,
                max_altitude_feet=10433,
                best_season="spring_autumn",
                price_usd=Decimal('1999.00'),
                discount_percentage=0,
                is_featured=False,
                is_popular=False,
                meta_description="Book the 15-Day Rara Lake Trek from Pokhara. Visit Nepal's largest lake in Rara National Park. Requires multiple domestic flights. Wilderness trekking.",
                meta_keywords="rara lake trek, rara national park, jumla trek, wilderness nepal, far western nepal, nepal's largest lake",
                image_keywords="Rara Lake view, national park, Mugu, pristine lake, remote trekking, horses, high altitude forest"
            )

            # Add itinerary for RLT (Pokhara start/end)
            rlt_days = [
                (1, "Arrival in Kathmandu", "Reach Kathmandu and settle in. Prepare for the morning flight.", "1400m", "0 hours", "Hotel in Kathmandu"),
                (2, "Final gear check and preparation (Kathmandu)", "Prepare gear and rest. Attend trek briefing. (Note: The trek requires domestic flights starting from Kathmandu.)", "1400m", "6-8 hours (drive)", "Hotel in Kathmandu"),
                (3, "Fly Kathmandu to Nepalgunj & to Jumla", "Morning flight from Kathmandu to Nepalgunj, followed by a connecting flight to Jumla (2,540m), the starting point of the trek. Overnight stay.", "2,540m", "2 hours (flying)", "Tea House/Guesthouse"),
                (4, "Trek to Danphe Lagna", "Begin the trek. The trail climbs steadily, passing through fields and small villages. Climb to the high ridge at Danphe Lagna.", "3,130m", "6-7 hours", "Tea House"),
                (5, "Trek to Chautha", "Descend through forests to a small stream. The trail then ascends through the thick pine forest of Rara National Park.", "2,770m", "6-7 hours", "Tea House"),
                (6, "Trek to Dhotu", "Descend to a valley bottom and ascend past a few small villages to Dhotu.", "2,380m", "5-6 hours", "Tea House"),
                (7, "Trek to Rara Lake (Rara Village)", "The final ascent to the ridge that overlooks Rara Lake. A spectacular view of the massive lake. Descend to the lake-side village for the night.", "3,010m", "6-7 hours", "Tea House/Lodge"),
                (8, "Exploration Day at Rara Lake", "Spend the day exploring the National Park and the circumference of the lake. Options include boating (if available) or hiking up to a nearby viewpoint.", "3,010m", "N/A", "Tea House/Lodge"),
                (9, "Rara to Murma", "Trek along the northern side of the lake to Murma. Enjoy views of the lake from a higher perspective.", "3,180m", "4-5 hours", "Tea House"),
                (10, "Murma to Ghorosingha", "A long day of descent through dense forests back toward the main trail.", "3,050m", "6-7 hours", "Tea House"),
                (11, "Trek to Sinja Valley", "The trail descends sharply into the Sinja Valley, an ancient capital of the Khasa Kingdom.", "2,490m", "5-6 hours", "Tea House"),
                (12, "Trek to Jumla", "The final day of trekking, retracing steps and following the main trail back to Jumla.", "2,540m", "6-7 hours", "Tea House/Guesthouse"),
                (13, "Fly Jumla to Nepalgunj & to Kathmandu", "Early morning flight from Jumla to Nepalgunj, followed by the connecting flight back to Kathmandu. Transfer to hotel.", "1,400m", "2 hours (flying)", "Hotel in Kathmandu"),
                (14, "Free Day in Kathmandu", "A buffer day to accommodate potential flight delays in the remote western sectors. Optional sightseeing or rest.", "1,400m", "N/A", "Hotel in Kathmandu"),
                (15, "Departure from Kathmandu via Pokhara Transfer", "Transfer from Kathmandu to Pokhara via tourist bus (included) or domestic flight (excluded). Final departure or onward journey from Pokhara.", "820m", "6-8 hours (travel)", "Not Included"),
            ]

            for day_num, title, desc, alt, hours, acc in rlt_days:
                Itinerary.objects.create(
                    trek=rlt, day_number=day_num, title=title, description=desc, altitude=alt, trekking_hours=hours, accommodation=acc, meals_included="Breakfast, Lunch, Dinner"
                )

            # Add included items for RLT
            rlt_included = [
                "Kathmandu to Pokhara/Pokhara to Kathmandu transportation (Tourist Bus - included)",
                "Domestic Flights: Kathmandu-Nepalgunj-Jumla (Roundtrip, total 4 flights)",
                "Rara National Park Entry Permit and TIMS Card",
                "Experienced, government-licensed, English-speaking trekking guide",
                "Porter service (1 porter for 2 trekkers, maximum weight 20kg)",
                "8 nights accommodation during the trek (basic tea houses/lodges)",
                "Accommodation in Kathmandu (Day 1, 2, 13, 14 - Hotel with breakfast)",
                "Accommodation in Nepalgunj/Jumla (Day 3, 12 - Guesthouse/Hotel with breakfast)",
                "3 meals a day (Breakfast, Lunch, Dinner) during the trek",
                "Staff costs (insurance, salary, equipment, food, and accommodation for all staff)",
                "Comprehensive first aid kit",
                "Farewell dinner in Kathmandu"
            ]

            for idx, item in enumerate(rlt_included, 1):
                IncludedItem.objects.create(trek=rlt, item=item, order=idx)

            # Add excluded items for RLT
            rlt_excluded = [
                "International airfare to/from Kathmandu",
                "Nepal entry visa fee (obtainable on arrival at TIA)",
                "Domestic flight from Kathmandu to Pokhara (Approx. USD $100-120) on Day 1 or 15 (Bus included)",
                "Travel and rescue insurance (mandatory)",
                "Personal expenses (bottled water, soft drinks, alcoholic beverages, phone calls, laundry, Wi-Fi/battery charging, hot showers)",
                "Tips for guide and porter (expected)",
                "Extra costs due to weather-related flight delays/cancellations (common in this region)",
                "Lunch/Dinner in Kathmandu and Pokhara (except farewell dinner)"
            ]

            for idx, item in enumerate(rlt_excluded, 1):
                ExcludedItem.objects.create(trek=rlt, item=item, order=idx)

            # Add map coordinates for RLT
            rlt_coords = [
                ("Pokhara", Decimal('28.2096'), Decimal('83.9856')),
                ("Kathmandu", Decimal('27.7172'), Decimal('85.3240')),
                ("Jumla", Decimal('29.2743'), Decimal('82.1812')),
                ("Danphe Lagna", Decimal('29.2905'), Decimal('82.2858')),
                ("Rara Lake", Decimal('29.5085'), Decimal('82.9090')),
                ("Murma", Decimal('29.5420'), Decimal('82.8950')),
                ("Sinja Valley", Decimal('29.2310'), Decimal('82.1550')),
            ]

            for idx, (name, lat, lng) in enumerate(rlt_coords, 1):
                MapCoordinate.objects.create(trek=rlt, name=name, latitude=lat, longitude=lng, order=idx)
            
            self.stdout.write(self.style.SUCCESS("✅ Rara Lake Trek Data loaded."))


            self.stdout.write(self.style.SUCCESS("✅ All 9 Trek objects created."))

        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f"Data loading failed (IntegrityError): {e}"))
            self.stdout.write(self.style.NOTICE("Action: You must run Trek.objects.all().delete() in the Django shell and try again."))
            return 
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred during data creation: {e}"))
            return
            
        
        # --- 2. IMAGE LOADING SECTION (FIXED: Added .strip() to handle trailing spaces) ---
        self.stdout.write(self.style.WARNING("\nStarting image loading and linking (using .strip() for robust title matching)..."))
        
        for folder_slug, trek_title_raw in TREK_FOLDERS.items():
            
            # CRITICAL FIX: Strip whitespace from the dictionary value before looking up the trek
            trek_title = trek_title_raw.strip() 
            
            try:
                # 1. Get the Trek instance 
                # Use the stripped title to match the title stored in the database
                trek_instance = Trek.objects.get(title=trek_title)
                
                # 2. Define the path to the current trek's image folder
                trek_folder_path = MEDIA_BASE / folder_slug
                
                # --- HERO IMAGE LOGIC (Single image) ---
                hero_file = trek_folder_path / 'hero.jpg'
                if hero_file.exists():
                    # Delete any previous hero image file (optional, for cleanup)
                    if trek_instance.hero_image:
                        # Only delete the file if it exists in storage to prevent errors
                        if os.path.exists(trek_instance.hero_image.path):
                             trek_instance.hero_image.delete(save=False) 
                        
                    # Django's ImageField.save needs an open file object AND a relative filename
                    relative_name = f'{folder_slug}/{hero_file.name}'
                    with open(hero_file, 'rb') as f:
                        trek_instance.hero_image.save(relative_name, File(f), save=True)
                    self.stdout.write(self.style.SUCCESS(f" - Saved HERO for {trek_title}"))
                else:
                    self.stdout.write(self.style.NOTICE(f" - HERO file not found at {hero_file}"))
                
                # --- GALLERY IMAGE LOGIC (Multiple images) ---
                # Clear existing gallery images for this trek before adding new ones
                TrekImage.objects.filter(trek=trek_instance).delete() 
                
                # Use glob to find all gallery files, handling both .jpg and .webp
                gallery_files = sorted(
                    list(trek_folder_path.glob('gallery-*.jpg')) + 
                    list(trek_folder_path.glob('gallery-*.webp'))
                )

                if gallery_files:
                    for index, file_path in enumerate(gallery_files):
                        relative_name = f'{folder_slug}/{file_path.name}'
                        
                        with open(file_path, 'rb') as f:
                            TrekImage.objects.create(
                                trek=trek_instance,
                                image=File(f, name=relative_name), 
                                caption=f"{trek_title} Gallery Image {index + 1}",
                                order=index + 1
                            )
                        self.stdout.write(f"    |-- Added gallery image: {file_path.name}")
                else:
                    self.stdout.write(self.style.NOTICE(f" - No gallery files found for {trek_title}"))
                        
            except Trek.DoesNotExist:
                # Now this only triggers if a trek wasn't created in the previous section (Section 1)
                self.stdout.write(self.style.ERROR(f"FATAL: Trek object missing for image linking: {trek_title}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing images for {trek_title}: {e}"))

        self.stdout.write(self.style.SUCCESS("\n✅ FINAL: All data loading and image linking complete!"))