# Analysis-of-Third-Party-Cookies-and-Requests-of-Top-1000-Sites

**Description**  
Almost every site asks you to accept their cookies. Most people accept them without thought. But what do these cookies actually do? With increasing concerns around trackers and privacy, I set out to identify the top 10 most common requests and cookies by searching through the top 1000 most frequented web sites and counting the number of occurances of each cookie. I consider a third-party entity one that does not share the same second-level domain as the intended site. For example, when visiting google.com, ads.google.com is not a third-party since it has the same second level domain (google) as google.com. However, doubleclick.net is considered a third-party to google.com.

**Objective:** To identify and tally the third-party cookies and requests accessed by the top 1000 most frequented websites.

**Method**  
_Scraper.py_ - Crawls through first 1000 sites in the top-1m.csv file and captures network traffic of each site as HAR files
_tp_requests.py_ - Parses each HAR file and identifies/counts each third-party request.
_tp_cookies.py_ - Parses each HAR file and identifies/counts each third-party cookie.

**Dependencies**  
Browsermob Proxy with Selenium Webdriver (Java 11 required for Browsermob Proxy)
Binary required for proxy to initialize browsermob server instance (folder attached)

**Results**

**The top 10 most commonly seen third-party cookies (and their intended functionality) are:**

AKA_A2(seen 1718 times): This cookie is used for Advanced Acceleration (performance), which allows for HTTP2 Push and DNS Prefetch.

At_check(seen 1127 times): This cookie is used by Adobe Target to see whether or not cookies are enabled or supported on the user’s browser.

s_cc(seen 801 times): This cookie is typically associated with Adobe SiteCatalyst, and checks if cookies are enabled in the user’s browser.

mscc(seen 549 times): This cookie is used by Microsoft. Its intended function varies, but generally is used to store unique identifiers for Microsoft’s services.

_sp_su(seen 414 times): The purpose of this cookie is unknown.

_gat(seen 413 times): This cookie is associated with Google Universal Analytics, used for performance via throttling the request rate (limits the collection of data on sites with high traffic).

usprivacy(seen 393 times): This cookie is used by the IAB CCPA Compliance Framework to store whether or not the user opted out of sale of personal data.

AMCVS_EA76ADE95776D2EC7F000101%40AdobeOrg(seen 386 times): This cookie stores a unique visitor identifier.

MC1(seen 335 times): Used by Microsoft to keep statistics on what pages the user has visited and how often an ad click leads to a purchase or other actions on the advertiser’s website.

MS0(seen 335 times): Used by Microsoft to keep statistics on what pages the user has visited and how often an ad click leads to a purchase or other actions on the advertiser’s website.
<br>
<br>
<br>
**The top 10 most commonly seen third-party domains are:**

googleapis - Seen 427 times.  
Googletagmanager - Seen 331 times.  
google - Seen 312 times.  
google-analytics - Seen 260 times.  
g - Seen 257 times.  
gstatic - Seen 170 times.  
onetrust - Seen 159 times.  
cookielaw - Seen 138 times.  
bing - Seen 122 times.  
facebook - Seen 121 times.  
