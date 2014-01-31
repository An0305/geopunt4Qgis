# -*- coding: utf-8 -*-
"""
/***************************************************************************
 geopunt
                                 
 "bibliotheek om geopunt in python te gebruiken"
                             -------------------
        begin                : 2013-12-05
        copyright            : (C) 2013 by Kay Warrie
        email                : kaywarrie@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import urllib2, urllib, json, sys, os.path, datetime

class Adres:
  def __init__(self, timeout=15):
    self.timeout = timeout
    self._locUrl = "http://loc.api.geopunt.be/geolocation/Location?"
    self._sugUrl = "http://loc.api.geopunt.be/geolocation/Suggestion?"

  def _createLocationUrl(self, q, c=1):
      geopuntUrl = self._locUrl
      data = {}
      data["q"] = unicode(q).encode('utf-8')
      data["c"] = c
      values = urllib.urlencode(data)
      result = geopuntUrl + values
      return result

  def fetchLocation(self, q, c=1):
      url = self._createLocationUrl(q, c=1)
      try:
            response = urllib2.urlopen(url, timeout=self.timeout)
      except (urllib2.HTTPError, urllib2.URLError) as e:
            return str( e.reason )
      except:
            return  str( sys.exc_info()[1] )
      else:
            LocationResult = json.load(response)
            return LocationResult["LocationResult"]

  def _createSuggestionUrl(self, q, c=5):
      geopuntUrl = self._sugUrl
      data = {}
      data["q"] = unicode(q).encode('utf-8')
      data["c"] = c
      values = urllib.urlencode(data)
      result = geopuntUrl + values
      return result

  def fetchSuggestion(self, q, c=5):
      url = self._createSuggestionUrl(q,c)
      try:
            response = urllib2.urlopen(url, timeout=self.timeout)
      except (urllib2.HTTPError, urllib2.URLError) as e:
            return str( e.reason )
      except:
            return  str( sys.exc_info()[1] )
      else:
            suggestion = json.load(response)
            return suggestion["SuggestionResult"]


      url = self._createSuggestionUrl(q,c)
      try:
	    response = urllib2.urlopen(url, timeout=self.timeout)
      except (urllib2.HTTPError, urllib2.URLError) as e:
	    return str( e.reason )
      except:
	    return  str( sys.exc_info()[1] )
      else:
	    suggestion = json.load(response)
	    return suggestion["SuggestionResult"]

class Poi:
  def __init__(self, timeout=15):
      self.timeout = timeout
      self._poiUrl = "http://poi.api.geopunt.be/core?"
      self.resultCount = 0
      
      #maxBounds srs 31370: x between 17736 and 297289, y between 23697 and 245375 
      #TODO: What if no Lambert coordinates as input???
      self.maxBounds = [17750,23720,297240,245340]  
      self.resultBounds = [17736,23697,297289,245375]
      self.PoiResult = []
      self.qeury = ""
      self.srs = 31370
      self.maxModel=True
      
  def _createPoiUrl(self , q, c=5, srs=31370 , maxModel=False, bbox=None, POItype='' ):
      poiUrl = self._poiUrl
      data = {}
      data["label"] = unicode(q).encode('utf-8')
      data["srsOut"] = srs
      data["srsIn"] = srs    #i am asuming srsIn wil alwaysbe = srsOut
      data["maxcount"] = c
      data["POItype"]  = POItype
      if maxModel:
	    data["maxModel"] = "true"
      else:
	    data["maxModel"] = "false"
      if bbox:
	    if bbox[0] < self.maxBounds[0]: 
	       bbox[0] = self.maxBounds[0]
	    if bbox[1] < self.maxBounds[1]:
	       bbox[1] = self.maxBounds[1]
	    if bbox[2] > self.maxBounds[2]:
	       bbox[2] = self.maxBounds[2]
	    if bbox[3] > self.maxBounds[3]:
	       bbox[3] = self.maxBounds[3]
	    data["bbox"] = "|".join([str(b) for b in bbox])
	
      values = urllib.urlencode(data)
      result = poiUrl + values
      return result
    
  def fetchPoi(self, q,  c=5, srs=31370, maxModel=True , updateResults=True, bbox=None, POIType='' ):
        url = self._createPoiUrl( q, c, srs, maxModel, bbox, POIType)
        try:
	        response = urllib2.urlopen(url, timeout=self.timeout)
        except urllib2.HTTPError as e:
	        return json.load(e)["Message"]
        except urllib2.URLError as e:
	        return str( e.reason )
        except:
	        return  str( sys.exc_info()[1] )
        else:
	    poi = json.load(response)
	
	    if updateResults:
	        self.resultCount =  int( poi["label"]["value"] )
	        if bbox:
	            self.resultBounds = bbox
	        else:
	            self.resultBounds = self._getBounds(poi["pois"])
	        self.PoiResult = poi["pois"]
	        self.qeury = q
	        self.srs = srs
	        self.maxModel = maxModel
	    return poi["pois"]
  
  def poiSuggestion(self):
      if self.PoiResult: 
	sug = self.PoiResult
      else: 
	return []
      i = 0
      if self.maxModel: 
	i = 1
      if sug.__class__ == str:
	return sug
      else:
        labels = [(n["id"], n["categories"][i]['value'],n["labels"][0]["value"],
		     n['location']['address']["value"]) for n in sug ] 
        labels.sort()
        return labels
    
  def _getBounds(self, poiResult ):
      minX = 1.7976931348623157e+308
      maxX = -1.7976931348623157e+308
      minY = 1.7976931348623157e+308
      maxY = -1.7976931348623157e+308
      
      points =  [n['location']['points'][0]['Point']['coordinates'] for n in poiResult ]
      for xy in points:
	    x, y = xy
	    if x > maxX: maxX = x
	    elif x < minX: minX = x
	    if y > maxY: maxY = y
	    elif y < minY: minY = y
	
      return [ minX, minY, maxX, maxY]

class gipod:
  def __init__(self, timeout=15):
      self.timeout = timeout
      self.baseUri = 'http://gipod.api.agiv.be/ws/v1/'
  
  def getCity(self, q="" ):
      query = urllib.quote(q)
      url = self.baseUri + "referencedata/city/" + query 
      try:
	  response = urllib2.urlopen(url, timeout=self.timeout)
      except (urllib2.HTTPError, urllib2.URLError) as e:
	  raise geopuntError(str( e.reason ))
      except:
	  raise geopuntError( str( sys.exc_info()[1] ))
      else:
	  city = json.load(response)
	  return city

  def getProvince(self, q="" ):
      query = urllib.quote(q)
      url = self.baseUri + "referencedata/province/" + query
      try:
	  response = urllib2.urlopen(url, timeout=self.timeout)
      except (urllib2.HTTPError, urllib2.URLError) as e:
	  raise geopuntError(str( e.reason ))
      except:
	  raise geopuntError( str( sys.exc_info()[1] ))
      else:
	  province = json.load(response)
	  return province

  def getEventType(self, q="" ):
      query = urllib.quote(q)
      url = self.baseUri + "referencedata/eventtype/" + query
      try:
	  response = urllib2.urlopen(url, timeout=self.timeout)
      except (urllib2.HTTPError, urllib2.URLError) as e:
	  raise geopuntError( str( e.reason ))
      except:
	  raise geopuntError( str( sys.exc_info()[1] ))
      else:
	  eventtype = json.load(response)
	  return eventtype

  def getOwner(self, q=''):
      query = urllib.quote(q)
      url = self.baseUri + "referencedata/owner/" + query
      try:
	  response = urllib2.urlopen(url, timeout=self.timeout)
      except (urllib2.HTTPError, urllib2.URLError) as e:
	  raise geopuntError( str( e.reason ))
      except:
	  raise geopuntError( str( sys.exc_info()[1] ))
      else:
	  owner = json.load(response)
	  return owner

  def _createWorkassignmentUrl(self, owner="", startdate=None, enddate=None, city="", province="", srs=31370, bbox=[], c=50, offset=0 ):
      "startdate and enddate are datetime.date\n bbox is [xmin,ymin,xmax,ymax]"
      endpoint = self.baseUri + 'workassignment?'
      data = {}
      data['limit'] = c
      if offset:
	data["offset"] = offset
      if owner:
	data['owner'] = owner
      if startdate and isinstance(startdate, datetime.date): 
	data["startdate"] = startdate.__str__()
      if enddate and isinstance(enddate, datetime.date): 
	data["enddate"] = enddate.__str__()
      if city:
	data['city'] = city
      if province:
	data['province'] = province
      if srs in [31370,4326,3857]:
	data['CRS'] = srs
      if bbox and isinstance(bbox,(list,tuple)) and len(bbox) == 4:
	xmin,ymin,xmax,ymax = bbox
	xymin = str(xmin) +','+ str(ymin)
	xymax = str(xmax) +','+ str(ymax)
	data["bbox"] = '|'.join(xymin,xymax)
      values = urllib.urlencode(data)
      result = endpoint + values
      return result

  def fetchWorkassignment(self,owner="", startdate=None, enddate=None, city="", province="", srs=31370, bbox=[], c=50, offset=0 ):
      url = self._createWorkassignmentUrl(owner, startdate, enddate, city, province, srs, bbox, c, offset )
      try:
	    response = urllib2.urlopen(url, timeout=self.timeout)
      except  (urllib2.HTTPError, urllib2.URLError) as e:
	    raise geopuntError( str( e.reason ))
      except:
	    raise geopuntError( str( sys.exc_info()[1] ))
      else:
	    workassignment = json.load(response)
	    return workassignment
	  
  def allWorkassignments(self, owner="", startdate=None, enddate=None, city="", province="", srs=31370, bbox=[]):
      counter = 0
      wAs = self.fetchWorkassignment(owner, startdate, enddate, city, province, srs, bbox, 100, counter )
      wAlen = len(wAs)
      while wAlen == 100:
	  counter += 100
	  wA = self.fetchWorkassignment(owner, startdate, enddate, city, province, srs, bbox, 100, counter )
	  wAs += wA
	  wAlen = len(wA)
      return wAs

  def _createManifestationUrl(self, owner="", eventtype="", startdate=None, enddate=None, city="", province="", srs=31370, bbox=[], c=50, offset=0 ):
      endpoint = self.baseUri + "manifestation?"
      data = {}
      data['limit'] = c
      if offset:
	data["offset"] = offset
      if owner:
	data['owner'] = owner
      if eventtype:
	data['eventtype'] = eventtype
      if startdate and isinstance(startdate, datetime.date): 
	data["startdate"] = startdate.__str__()
      if enddate and isinstance(enddate, datetime.date): 
	data["enddate"] = enddate.__str__()
      if city:
	data['city'] = city
      if province:
	data['province'] = province
      if srs in [31370,4326,3857]:
	data['CRS'] = srs
      if bbox and isinstance(bbox,(list,tuple)) and len(bbox) == 4:
	xmin,ymin,xmax,ymax = bbox
	xymin = str(xmin) +','+ str(ymin)
	xymax = str(xmax) +','+ str(ymax)
	data["bbox"] = '|'.join(xymin,xymax)
      values = urllib.urlencode(data)
      result = endpoint + values
      return result
  
  def fetchManifestation(self, owner="", eventtype="", startdate=None, enddate=None, city="", province="", srs=31370, bbox=[], c=50, offset=0 ):
      url = self._createManifestationUrl(owner, eventtype, startdate, enddate, city, province, srs, bbox, c, offset )
      try:
	    response = urllib2.urlopen(url, timeout=self.timeout)
      except  (urllib2.HTTPError, urllib2.URLError) as e:
	    raise geopuntError( str( e.reason ))
      except:
	    raise geopuntError( str( sys.exc_info()[1] ))
      else:
	    manifestation = json.load(response)
	    return manifestation
	  
  def allManifestations(self, owner="", eventtype="", startdate=None, enddate=None, city="", province="", srs=31370, bbox=[]):
      counter = 0
      mAs = self.fetchManifestation(owner, eventtype, startdate, enddate, city, province, srs, bbox, 100, counter )
      mAlen = len(mAs)
      while mAlen == 100:
	  counter += 100
	  mA = self.fetchManifestation(owner, eventtype, startdate, enddate, city, province, srs, bbox, 100, counter )
	  mAs += mA
	  mAlen = len(mA)
      return mAs
  
class geopuntError(Exception):
    def __init__(self, message):
	  self.message = message
    def __str__(self):
	  return repr(self.message)
	  
def internet_on(timeout=15):
    try:
	    response=urllib2.urlopen('http://loc.api.geopunt.be',timeout=timeout)
	    return True
    except: 
	    return False