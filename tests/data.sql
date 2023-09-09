INSERT INTO user (id , username, password, email, country)
VALUES
  (1, 'test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'test@example.com', 'Argentina'),
  (2, 'other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79', 'other@example.com', 'United Kingdom');


INSERT INTO log (tid, lifter_id, tday, exercise, weight, sets ,reps)
VALUES
  (1, 1,'04-04-2023', 'Squat', '100', '5', '5');

INSERT into pwreset(id, reset_key, user_id, datetime, has_activated)
VALUES
(1, 'resetresetreset', 1, '2023-09-09', 0)
 