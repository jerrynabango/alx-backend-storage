-- script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

DELIMITER |

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
  UPDATE users AS User, 
    (SELECT User.id, SUM(score * weight) / SUM(weight) AS w_avg 
    FROM users AS User 
    JOIN corrections as Compute ON User.id=Compute.user_id 
    JOIN projects AS P ON Compute.project_id=P.id 
    GROUP BY User.id)
  AS Weighted_Avgs
  SET User.average_score = Weighted_Avgs.w_avg 
  WHERE User.id=Weighted_Avgs.id;
END;
