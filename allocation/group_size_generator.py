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

class ImpossibleConstraintsError(Exception):
    """
        Raised when group sizes are provided which
        cannot be met.
    """
    pass

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

def attempt_to_form_ideal_groups(no_people, ideal_size):
    """
        Forms the maximum number of ideally sized groups given
        the number of people.

        Returns tuple containing the a list of formed groups and the
        number of people remaining after the groups were formed.
        
        attempt_to_form_ideal_groups(int, int) -> (int, list(Group))
    """
    no_groups, remaining_people = divmod(no_people, ideal_size)
    groups = [Group(ideal_size) for i in range(no_groups)]
    
    return (remaining_people, groups)

def attempt_to_form_smaller_groups(no_people, ideal_size, min_size):
    """
        Attempts to form smaller groups as close to the ideal
        size using the given number of people.

        Returns a tuple containing the number of people remaining 
        after the attempt and a list of groups that were formed.

        attempt_to_form_smaller_groups(int, int, int) -> (int, list(Group))
    """
    formed_groups = []
    current_size = ideal_size - 1
    
    while current_size >= min_size:
        if no_people >= current_size:
            formed_groups.append(Group(current_size))
            no_people -= current_size
        current_size -= 1

    return (no_people, formed_groups)

def attempt_to_add_to_existing_groups(no_people, existing_groups, max_size):
    """
        Attempts to add the given number of people to the list of
        existing groups without exceeding the maximum group size.

        Modifies the list of existing groups. Returns the number of people
        remaining after the attempt.

        attempt_to_add_to_existing_groups(int, list(Group), int) -> int
    """
    for group in existing_groups:
        if no_people == 0:
            break

        # We want to add as many people to the group as possible
        max_that_can_be_added = max_size - group.get_size()
        amount_that_can_be_added = min(no_people, max_that_can_be_added)
        group.alter_size(amount_that_can_be_added)
        no_people -= amount_that_can_be_added
    
    return no_people

def attempt_to_form_min_sized_group_from_existing(no_people, existing_groups, min_size):
    """
        Attempts to form a minimum sized group using the given number
        of people by extracting people from the existing groups. People will
        only be removed from groups that are able to lose people.

        Returns the number of people remaining after the attempt is made.

        attempt_to_form_min_sized_group_from_existing(int, list(Group), int) -> int
    """
    if no_people == 0:
        return no_people
    
    people_needed = min_size - no_people
    people_that_can_be_moved = 0

    # We need to know whether or not we are able to remove
    # enough people to form this new group
    groups_being_removed_from = []
    
    for index, group in enumerate(existing_groups):
        if group.get_size() > min_size:
            max_people_to_move = group.get_size() - min_size
            no_people_shifted = \
                min(max_people_to_move, people_needed - people_that_can_be_moved)

            if no_people_shifted > 0:
                people_that_can_be_moved += no_people_shifted
                groups_being_removed_from.append((index, no_people_shifted))

                if people_that_can_be_moved >= people_needed:
                    break
    
    # If there aren't enough people, we don't want to modify anything
    if people_that_can_be_moved < people_needed:
        return no_people
    
    # If there are enough people, extract them and add the new group to
    # the list of existing groups
    for index, amount in groups_being_removed_from:
        existing_groups[index].alter_size(-amount)
    
    existing_groups.append(Group(min_size))

    return 0
    
def collate_formed_groups(created_groups):
    """
        Collates the created groups into a usable summary
    
        collate_formed_groups(list(Group)) -> dict(int : int)
    """
    collated_result = {}
    
    for group in created_groups:
        if group.get_size() not in collated_result:
            collated_result[group.get_size()] = 1
        else:
            collated_result[group.get_size()] += 1

    return collated_result

def determine_group_numbers(no_people, min_size, ideal_size, max_size):
    """
        Attempts to generate a list of group sizes within the given
        size parameters to fit no_people into. 

        If successful, returns a dictionary containing the group sizes
        to be formed and the number of groups of that size to make.
        If it is not possible to form groups to match the given
        constaints, raises an ImpossibleConstraintsError.
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
    # so we try to form ideal sized groups first
    remaining_people, ideal_groups = \
        attempt_to_form_ideal_groups(no_people, ideal_size)
    formed_groups.extend(ideal_groups)

    #no_ideal_groups, remaining_people = divmod(no_people, ideal_size)

    #for i in range(no_ideal_groups):
    #    formed_groups.append(Group(ideal_size))
    
    # Now, remaining_people < ideal_size
    # We have two options, we can either form smaller groups, or add the
    # remaining people to the existing groups
    
    remaining_people, smaller_groups = \
        attempt_to_form_smaller_groups(remaining_people, ideal_size, min_size)
    formed_groups.extend(smaller_groups)


    #current_size = ideal_size - 1
    #while current_size > min_size:
        # See if we can make a group of this size. If we can, then
        # make it since it will maximise the number of ideal groups
    #    if current_size == remaining_people:
    #        formed_groups.append(Group(current_size))
    #        remaining_people = 0
    #    current_size -= 1
    
    #if remaining_people > 0:
        # We've failed to create smaller groups within acceptable
        # parameters that use all remaining people. So instead, we 
        # try to increase the size of the other groups. 

        # First, we see if we can add all of the remaining people
        # into a single ideal group. This maximises the number of
        # ideal groups
    #    for group in formed_groups:
    #        if remaining_people + group.get_size() <= max_size:
    #            group.alter_size(remaining_people)
    #            remaining_people = 0
    
    remaining_people = \
        attempt_to_add_to_existing_groups(remaining_people, formed_groups, max_size)

    #if remaining_people > 0:
        # We can't add all the people into a single ideal group
        # So instead we try to add as many people into the ideal
        # groups systematically
    #    for group in formed_groups:
    #        space_left = max_size - group.get_size()

    #        while space_left > 0 and remaining_people > 0:
    #            group.increment_size()
    #            remaining_people -= 1
    #            space_left = max_size - group.get_size()

    remaining_people = \
        attempt_to_form_min_sized_group_from_existing(remaining_people, formed_groups, min_size)

    if remaining_people > 0:
        raise ImpossibleConstraintsError()
    
    #if remaining_people > 0:
        # If we're in here, it means that we've failed to make
        # smaller and larger groups and still have people remaining.
        # The only option left is to try and break people out of
        # groups in order to form another group of minimum size
    #    people_needed = min_size - remaining_people
    #    people_that_can_be_moved = 0

        # We need to know whether or not we are able to remove
        # enough people to form this new group
    #    group_indices = []
    #    for index, group in enumerate(formed_groups):
    #        if group.get_size() > min_size:
    #            max_people_to_move = group.get_size() - min_size
    #            people_shifted = min(max_people_to_move, people_needed - people_that_can_be_moved)

    #            if people_shifted > 0:
    #                people_that_can_be_moved += people_shifted
    #                group_indices.append((index, people_shifted))

    #            if people_that_can_be_moved >= people_needed:
    #                break
        
        # If we dont have enough people, then it's impossible.
        # Otherwise, we remove the people needed
    #    if people_that_can_be_moved < people_needed:
    #        raise ValueError("Impossible Constraints")
    #    else:
    #        for index, amount in group_indices:
    #            formed_groups[index].alter_size(-amount)
    #        formed_groups.append(Group(min_size))

    #final_result = {}
    
    #for group in formed_groups:
    #    if group.get_size() not in final_result:
    #        final_result[group.get_size()] = 1
    #    else:
    #        final_result[group.get_size()] += 1

    #return final_result   
    return collate_formed_groups(formed_groups) 
                
#print(determine_group_numbers(20, 3, 4, 5))
#print(determine_group_numbers(5531, 18, 24, 38))
#print(determine_group_numbers(10, 4, 4, 5))
#print(determine_group_numbers(56, 3, 54, 55))
#print(determine_group_numbers(15, 8, 9, 10))

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
