DELETE FROM auth_user;    
DELETE FROM sqlite_sequence WHERE NAME='auth_user';

DELETE FROM authtoken_token;    
DELETE FROM sqlite_sequence WHERE NAME='authtoken_token';

DELETE FROM rareapi_post;    
DELETE FROM sqlite_sequence WHERE NAME='rareapi_post';

DELETE FROM rareapi_rareuser;    
DELETE FROM sqlite_sequence WHERE NAME='rareapi_rareuser';

DELETE FROM rareapi_category;    
DELETE FROM sqlite_sequence WHERE NAME='rareapi_category';

DELETE FROM rareapi_tag;    
DELETE FROM sqlite_sequence WHERE NAME='rareapi_tag';
