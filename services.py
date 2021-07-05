'''
an abstraction layer between the database model and the app
also contains helper functions for the app
'''
#Imports
from datetime import date, datetime
import dateutil.parser
import babel
from sqlalchemy.sql.expression import true
from schema import *

#Functions
def format_datetime(value, format='medium'):
    '''filter for date show'''
    date = dateutil.parser.parse(value)
    if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
      format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')

def get_boolean(s):
    if s is None:
        return False
    return True
#add data to the db
def add_venue(form_obj):
    '''
    adds a new venue to the database given data extracted from the form
    '''
    venue = Venue(name = form_obj.get('name'),
    city = form_obj.get('city'),
    state = form_obj.get('state'),
    address = form_obj.get('address'),
    phone = form_obj.get('phone'),
    image_link = form_obj.get('image_link'),
    facebook_link = form_obj.get('facebook_link'),
    website = form_obj.get('website'),
    genres = form_obj.getlist('genres'),
    seeking_talent = form_obj.get('seeking_talent'),
    seeking_talent_description = form_obj.get('seeking_talent_description'))
    try:
        db.session.add(venue)
        db.session.commit()
    except Exception as e:
        print(e)
        return db.session.rollback()
    return venue

def add_artist(form_obj):
    '''
    adds a new artist to the database given data extracted from the form
    '''
    artist = Artist(name = form_obj['name'],
    city = form_obj.get('city'),
    state = form_obj.get('state'),
    phone = form_obj.get('phone'),
    image_link = form_obj.get('image_link'),
    facebook_link = form_obj.get('facebook_link'),
    website = form_obj.get('website'),
    genres = form_obj.getlist('genres'),
    seeking_venue = form_obj.get('seeking_venue'),
    seeking_venue_description = form_obj.get('seeking_venue_description'))
    try:
        db.session.add(artist)
        db.session.commit()
    except Exception as e:
        print(e)
        return db.session.rollback()
    return artist

def add_show(artist_id, venue_id, start_date):
    '''creates new show and insert it to the database'''
    show = Show(artist_id = artist_id, venue_id = venue_id, starts_at = start_date)
    try:
        db.session.add(show)
        db.session.commit()
    except Exception as e:
        print(e)
        return db.session.rollback()
    return show

#artists
def get_artist(id):
    '''get the artist of the required id'''
    res = Artist.query.get(id)
    return res
def get_artists():
    '''get all artists'''
    res = Artist.query.all()
    return res
def edit_artist_data(artist_id, new_data):
    '''
    edits an existing artist given data extracted from the form
    '''
    artist = get_artist(artist_id)
    artist.name = new_data.name.data
    artist.city = new_data.city.data
    artist.state = new_data.state.data
    artist.phone = new_data.phone.data
    artist.image_link = new_data.image_link.data
    artist.facebook_link = new_data.facebook_link.data
    artist.website = new_data.website.data
    artist.genres = new_data.genres.data
    artist.seeking_venue = new_data.seeking_venue.data
    artist.seeking_venue_description = new_data.seeking_venue_description.data
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return db.session.rollback()
    return artist

def get_artist_data(id):
    '''get details of an artist'''
    artist = get_artist(id)
    res = {}
    res['id'] = artist.id
    res['name'] = artist.name
    res['city'] = artist.city
    res['state'] = artist.state
    res['phone'] = artist.phone
    res['image_link'] = artist.image_link
    res['website'] = artist.website
    res['facebook_link'] = artist.facebook_link
    res['genres'] = artist.genres
    res['seeking_venue'] = artist.seeking_venue
    res['seeking_description'] = artist.seeking_venue_description
    res['past_shows'] = list(filter(lambda s : s.starts_at < datetime.now(), artist.shows))
    res['upcoming_shows'] = [s for s in artist.shows if s not in res['past_shows']]
    res['past_shows_count'] = len(res['past_shows'])
    res['upcoming_shows_count'] = len(res['upcoming_shows'])
    return res
def search_artists_query(q):
    '''search artists'''
    artists = Artist.query.filter(Artist.name.ilike('%'+q+'%')).all()
    res = {}
    res['count'] = len(artists)
    data = []
    for artist in artists:
        ele = {}
        ele['id'] = artist.id
        ele['name'] = artist.name
        ele['num_upcoming_shows'] = len(list(filter(lambda s : s.starts_at > datetime.now(), artist.shows)))
        data.append(ele)
    res['data'] = data
    return res
#venues
def get_venue(id):
    '''get venue of the required id'''
    res = Venue.query.get(id)
    return res
def edit_venue_data(venue_id, new_data):
    '''
    edits an existing venue given data extracted from the form
    '''
    venue = get_venue(venue_id)
    venue.name = new_data.name.data
    venue.city = new_data.city.data
    venue.state = new_data.state.data
    venue.address = new_data.address.data
    venue.phone = new_data.phone.data
    venue.image_link = new_data.image_link.data
    venue.facebook_link = new_data.facebook_link.data
    venue.website = new_data.website.data
    venue.genres = new_data.genres.data
    venue.seeking_talent = new_data.seeking_talent.data
    venue.seeking_talent_description = new_data.seeking_talent_description.data
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return db.session.rollback()
    return venue

def get_venue_data(id):
    '''get details of a required venue'''
    venue = get_venue(id)
    res = {}
    res['id'] = venue.id
    res['name'] = venue.name
    res['address'] = venue.address
    res['city'] = venue.city
    res['state'] = venue.state
    res['phone'] = venue.phone
    res['image_link'] = venue.image_link
    res['website'] = venue.website
    res['facebook_link'] = venue.facebook_link
    res['genres'] = venue.genres
    res['seeking_talent'] = venue.seeking_talent
    res['seeking_description'] = venue.seeking_talent_description
    res['past_shows'] = list(filter(lambda s : s.starts_at < datetime.now(), venue.shows))
    res['upcoming_shows'] = [s for s in venue.shows if s not in res['past_shows']]
    res['past_shows_count'] = len(res['past_shows'])
    res['upcoming_shows_count'] = len(res['upcoming_shows'])
    return res

def get_venues():
    '''get all venues grouped by city and state'''
    data = []
    venues = Venue.query.all()
    places = Venue.query.distinct(Venue.city, Venue.state).all()
    for place in places:
        data.append(
            {
                'city' : place.city,
                'state' : place.state,
                'venues' : [{
                    'id' : v.id,
                    'name' : v.name,
                    'num_upcoming_shows' : len(list(filter(lambda s : s.starts_at > datetime.now(), v.shows)))
                } for v in venues if v.city == place.city and v.state == place.state]
            }
        )
    return data
def search_venues_query(q):
    '''search venues'''
    venues = Venue.query.filter(Venue.name.ilike('%'+q+'%')).all()
    res = {}
    res['count'] = len(venues)
    data = []
    for venue in venues:
        ele = {}
        ele['id'] = venue.id
        ele['name'] = venue.name
        ele['num_upcoming_shows'] = len(list(filter(lambda s : s.starts_at > datetime.now(), venue.shows)))
        data.append(ele)
    res['data'] = data
    return res
def delete_venue_row(id):
    '''delete the required venue'''
    venue = get_venue(id)
    try:
        #delete the associated shows first
        Show.query.filter(Show.venue_id == venue.id).delete()
        db.session.delete(venue)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return db.session.rollback()

#shows
def list_shows():
    '''get all shows'''
    res = Show.query.all()
    return res

