-- script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

DELIMITER |

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
  UPDATE users AS User, 
    (SELECT User.id, SUM(score * weight) / SUM(weight) AS average 
    FROM users AS User 
    JOIN corrections as Compute ON User.id=Compute.user_id 
    JOIN projects AS Project ON Compute.project_id=Project.id 
    GROUP BY User.id)
  AS Weighted
  SET User.average_score = Weighted.average 
  WHERE User.id=Weighted.id;
END;
