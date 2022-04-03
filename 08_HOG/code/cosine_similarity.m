function [similarity] = cosine_similarity(object1,object2)
% Computes the degree of similarity between two objects using the cosine
% similarity
object1 = object1(:); % Transforms the matrix into a single column vector
object2 = object2(:); % Same concept

similarity = dot(object1,object2) / (norm(object1)*norm(object2));
end

