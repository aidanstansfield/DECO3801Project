"""
    Contains algorithms for determining the number of each size
    group to create.
"""
class Group:
    """
        Represents a basic group
    """
    def __init__(self, size):
        self.size = size
    
    def increment_size(self):
        self.size += 1
    
    def decrement_size(self):
        self.size -= 1
    
    def alter_size(self, amount):
        self.size += amount
    
    def get_size(self):
        return self.size
    
    def __repr__(self):
        return "Group (size {})".format(self.size)

def validate_entered_group_sizes(min_size, ideal_size, max_size):
    """
        Checks whether the entered group sizes are valid
        (i.e. 0 <= min_size <= ideal_size <= max_size)

        Raises a ValueError if the sizes are invalid
    """
    if min_size < 0:
        raise ValueError("min size cannot be negative") 
    if ideal_size < min_size:
        raise ValueError("ideal size cannot be less than minimum size")    
    if max_size < ideal_size:
        raise ValueError("max size cannot be less than ideal size")   

def determine_group_numbers(no_people, min_size, ideal_size, max_size):
    """
        Attempts to generate a list of group sizes within the given
        size parameters to fit no_people into. 

        If successful, returns a list of groups. Otherwise, if invalid
        parameters are provided, or it is impossible to generate groups
        within the given parameters, raises a ValueError.
    """

    if no_people < 0:
        ValueError("number of people cannot be negative")

    validate_entered_group_sizes(min_size, ideal_size, max_size)

    # We fail if there aren't enough people to allocate a minimum sized
    # group.
    if no_people < min_size:
        raise ValueError("There aren't enough people to allocate")
    
    formed_groups = []

    # We now know that there are enough people for a minimum sized group,
    # so we try to form ideal sized groups
    no_ideal_groups, remaining_people = divmod(no_people, ideal_size)

    for i in range(no_ideal_groups):
        formed_groups.append(Group(ideal_size))
    
    # Now, remaining_people < ideal_size
    # We have two options, we can either add the remaining people to
    # the existing groups, or form a smaller group
    
    current_size = ideal_size - 1
    while current_size > min_size:
        # See if we can make a group of this size. If we can, then
        # make it since it will maximise the number of ideal groups
        if current_size == remaining_people:
            formed_groups.append(Group(current_size))
            remaining_people = 0
        current_size -= 1
    
    if remaining_people > 0:
        # We've failed to create smaller groups within acceptable
        # parameters that use all remaining people. So instead, we 
        # try to increase the size of the other groups. 

        # First, we see if we can add all of the remaining people
        # into a single ideal group. This maximises the number of
        # ideal groups
        for group in formed_groups:
            if remaining_people + group.get_size() <= max_size:
                group.alter_size(remaining_people)
                remaining_people = 0
    
    if remaining_people > 0:
        # We can't add all the people into a single ideal group
        # So instead we try to add as many people into the ideal
        # groups systematically
        for group in formed_groups:
            space_left = max_size - group.get_size()

            while space_left > 0 and remaining_people > 0:
                group.increment_size()
                remaining_people -= 1
                space_left = max_size - group.get_size()

    if remaining_people > 0:
        # If we're in here, it means that we've failed to make
        # smaller and larger groups and still have people remaining.
        # The only option left is to try and break people out of
        # groups in order to form another group of minimum size
        people_needed = min_size - remaining_people
        people_that_can_be_moved = 0

        # We need to know whether or not we are able to remove
        # enough people to form this new group
        group_indices = []
        for index, group in enumerate(formed_groups):
            if group.get_size() > min_size:
                max_people_to_move = group.get_size() - min_size
                people_shifted = min(max_people_to_move, people_needed - people_that_can_be_moved)

                if people_shifted > 0:
                    people_that_can_be_moved += people_shifted
                    group_indices.append((index, people_shifted))

                if people_that_can_be_moved >= people_needed:
                    break
        
        # If we dont have enough people, then it's impossible.
        # Otherwise, we remove the people needed
        if people_that_can_be_moved < people_needed:
            raise ValueError("Impossible Constraints")
        else:
            for index, amount in group_indices:
                formed_groups[index].alter_size(-amount)
            formed_groups.append(Group(min_size))

    final_result = {}
    
    for group in formed_groups:
        if group.get_size() not in final_result:
            final_result[group.get_size()] = 1
        else:
            final_result[group.get_size()] += 1

    return final_result    
                
#determine_group_numbers(20, 3, 4, 5)
print(determine_group_numbers(5531, 18, 24, 38))
#determine_group_numbers(10, 4, 4, 5)
#determine_group_numbers(56, 3, 54, 55)
#determine_group_numbers(15, 8, 9, 10)

"""
    groups = []

    # We naively try to create as many ideal size groups
    no_ideal_groups, remaining_people = divmod(no_people, ideal_size)

    # If the min_size, ideal_size and max_size are the same and we
    # have people left over, then it's not possible
    if min_size == ideal_size and ideal_size == max_size and remaining_people != 0:
        raise ValueError("Impossible constraints")
    else:
        for i in range(no_ideal_groups):
            groups.append(Group(ideal_size))
   
    # With the remaining number of people, we can try and append them to the existing
    # groups of ideal size if it doesn't exceed the max size
    remaining_range = range(remaining_people)
    for i in remaining_range:
        if groups[i % len(groups)].size < max_size:
            groups[i % len(groups)].increment_size()
            remaining_people -= 1
   
    # If there are still people remaining, we try and form a new group of that size
    # If it isn't in the wanted range, we try and extract enough people to make
    # an ideal or minimum sized team without breaking other groups
    if remaining_people != 0:
        if remaining_people == min_size:
            groups.append(Group(remaining_people))
        elif remaining_people < min_size:
            people_to_extract = min_size - remaining_people
            people_extracted = 0

            group_copy = groups.copy()
            for i in range(people_to_extract):
                if groups[i % len(groups)].size > min_size:
                    groups[i % len(groups)].decrement_size()
                    people_extracted += 1
                if people_extracted == people_to_extract:
                    break
            
            if people_extracted == people_to_extract:
                for i in range(people_to_extract):
                    groups[i % len(groups)].decrement_size()
                groups.append(Group(min_size))
            else:
                raise ValueError("Impossible Constraints")
        else:
            groups.append(Group(remaining_people))

    print(groups)

"""
