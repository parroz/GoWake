from .models import LeaderBoard


def get_phase_pontuation(phase):
    global_pontuation = ''
    if phase == 'QLF':
        global_pontuation = '-Q_global_pontuation'
    elif phase == 'LCQ':
        global_pontuation = '-LCQ_global_pontuation'
    elif phase == 'QrtFinal':
        global_pontuation = '-QrtFinal_global_pontuation'
    elif phase == 'SemiFinal':
        global_pontuation = '-SemiFinal_global_pontuation'
    elif phase == 'Final':
        global_pontuation = '-Final_global_pontuation'

    return global_pontuation


def order_list_asc(phase):
    global_pontuation = ''
    if phase == 'QLF':
        global_pontuation = 'Q_global_pontuation'
    elif phase == 'LCQ':
        global_pontuation = 'LCQ_global_pontuation'
    elif phase == 'QrtFinal':
        global_pontuation = 'QrtFinal_global_pontuation'
    elif phase == 'SemiFinal':
        global_pontuation = 'SemiFinal_global_pontuation'
    elif phase == 'Final':
        global_pontuation = 'Final_global_pontuation'

    return global_pontuation


def set_ranking_pontuation(competition, gender, athlete_event, phase):
    leaderboards = LeaderBoard.objects.filter(
        competition=competition,
        athlete_category_in_competition=athlete_event.category_in_competition, athlete_gender=gender,
        Q_Heat_number=1, round=phase
    ).order_by('-Q_global_pontuation')

    index = 0
    for leaderboard in leaderboards:

        if index == 0 and leaderboard.global_pontuation > 0:
            leaderboard.ranking_event_final_points = 100
        if index == 1 and leaderboard.global_pontuation > 0:
            leaderboard.ranking_event_final_points = 80
        if index == 2 and leaderboard.global_pontuation > 0:
            leaderboard.ranking_event_final_points = 65
        if index == 3 and leaderboard.global_pontuation > 0:
            leaderboard.ranking_event_final_points = 55
        if index == 4 and leaderboard.global_pontuation > 0:
            leaderboard.ranking_event_final_points = 45
        if index == 5 and leaderboard.global_pontuation > 0:
            leaderboard.ranking_event_final_points = 35
        if index == 6 and leaderboard.global_pontuation > 0:
            leaderboard.ranking_event_final_points = 30
        if index == 7 and leaderboard.global_pontuation > 0:
            leaderboard.ranking_event_final_points = 25
        if index == 8 and leaderboard.global_pontuation > 0:
            leaderboard.ranking_event_final_points = 20
        if index == 9 and leaderboard.global_pontuation > 0:
            leaderboard.ranking_event_final_points = 17
        if index == 10 and leaderboard.global_pontuation > 0:
            leaderboard.ranking_event_final_points = 14
        if index == 11 and leaderboard.global_pontuation > 0:
            leaderboard.ranking_event_final_points = 11
        if index == 12 and leaderboard.global_pontuation > 0:
            leaderboard.ranking_event_final_points = 8
        if index == 13 and leaderboard.global_pontuation > 0:
            leaderboard.ranking_event_final_points = 6
        if index == 14 and leaderboard.global_pontuation > 0:
            leaderboard.ranking_event_final_points = 5
        if index == 15 and leaderboard.global_pontuation > 0:
            leaderboard.ranking_event_final_points = 4
        if index == 16 and leaderboard.global_pontuation > 0:
            leaderboard.ranking_event_final_points = 3
        if index == 17 and leaderboard.global_pontuation > 0:
            leaderboard.ranking_event_final_points = 2
        if index >= 18 and leaderboard.global_pontuation > 0:
            leaderboard.ranking_event_final_points = 1

        if leaderboard.global_pontuation == 0:
            leaderboard.ranking_event_final_points = 0

        leaderboard.save()
        index += 1


def set_new_leaderboard(round, leaderboard, idx, user):
    leader_board_new = LeaderBoard()
    leader_board_new.athlete = leaderboard.athlete
    leader_board_new.username = user
    leader_board_new.competition = leaderboard.competition
    leader_board_new.global_pontuation = leaderboard.global_pontuation
    leader_board_new.ranking = leaderboard.ranking
    leader_board_new.athlete_gender = leaderboard.athlete_gender
    leader_board_new.athlete_category_in_competition = leaderboard.athlete_category_in_competition
    leader_board_new.Q_1st_judge_atlhete_front_foot = leaderboard.Q_1st_judge_atlhete_front_foot
    leader_board_new.Q_1st_Judge_Last_name = leaderboard.Q_1st_Judge_Last_name
    leader_board_new.Q_1st_judge_first_name = leaderboard.Q_1st_judge_first_name
    leader_board_new.Q_1st_judge_iwwf_id = leaderboard.Q_1st_judge_iwwf_id
    leader_board_new.Q_2nd_judge_atlhete_front_foot = leaderboard.Q_2nd_judge_atlhete_front_foot
    leader_board_new.Q_2nd_Judge_Last_name = leaderboard.Q_2nd_Judge_Last_name
    leader_board_new.Q_2nd_judge_first_name = leaderboard.Q_2nd_judge_first_name
    leader_board_new.Q_2nd_judge_iwwf_id = leaderboard.Q_2nd_judge_iwwf_id
    leader_board_new.Q_3rd_judge_atlhete_front_foot = leaderboard.Q_3rd_judge_atlhete_front_foot
    leader_board_new.Q_3rd_Judge_Last_name = leaderboard.Q_3rd_Judge_Last_name
    leader_board_new.Q_3rd_judge_first_name = leaderboard.Q_3rd_judge_first_name
    leader_board_new.Q_3rd_judge_iwwf_id = leaderboard.Q_3rd_judge_iwwf_id
    leader_board_new.Q_Starting_list = idx
    leader_board_new.Q_Heat_number = 1
    leader_board_new.round = round
    leader_board_new.save()


def process_leaderboards_7_10(phase, competition, gender, athlete_event, user):
    i = 1
    leaderboards_lcq = []
    leaderboards_final = []
    while i < 3:
        leaderboards = LeaderBoard.objects.filter(
            competition=competition,
            athlete_category_in_competition=athlete_event.category_in_competition, athlete_gender=gender,
            Q_Heat_number=i, round=phase
        ).order_by('-Q_global_pontuation')

        leaderboards_final.extend(leaderboards[:2])
        leaderboards = leaderboards[2:]
        leaderboards_lcq.extend(leaderboards)
        i += 1
    idx = 1
    leaderboards_final.sort(key=lambda x: getattr(x, 'Q_global_pontuation'))

    for leaderboard in leaderboards_final:
        set_new_leaderboard('Final', leaderboard, idx, user)
        idx += 1
    idx = 1
    leaderboards_lcq.sort(key=lambda x: getattr(x, 'Q_global_pontuation'))
    for leaderboard in leaderboards_lcq:
        set_new_leaderboard('LCQ', leaderboard, idx, user)
        idx += 1


def process_leaderboards_7_10_LCQ(phase, competition, gender, athlete_event, user):
    leaderboards_final = []
    leaderboards = LeaderBoard.objects.filter(
        competition=competition,
        athlete_category_in_competition=athlete_event.category_in_competition, athlete_gender=gender,
        Q_Heat_number=1, round=phase
    ).order_by('-Q_global_pontuation')

    leaderboards_final.extend(leaderboards[:2])
    idx = 1
    for leaderboard in leaderboards_final:
        set_new_leaderboard('Final', leaderboard, idx, user)
        idx += 1

    finalists = LeaderBoard.objects.filter(
        competition=competition,
        athlete_category_in_competition=athlete_event.category_in_competition, athlete_gender=gender,
        Q_Heat_number=1, round='Final'
    ).order_by('global_pontuation')

    idx = 1
    for leaderboard in finalists:
        leaderboard.round = 'Final'
        leaderboard.Q_Starting_list = idx
        leaderboard.Q_Heat_number = 1
        leaderboard.save()
        idx += 1


def process_leaderboards_3_6(phase, competition, gender, athlete_event, user):
    leaderboards = LeaderBoard.objects.filter(
        competition=competition,
        athlete_category_in_competition=athlete_event.category_in_competition, athlete_gender=gender,
        Q_Heat_number=1
    ).order_by('-Q_global_pontuation')

    idx = 1
    for leaderboard in leaderboards:
        set_new_leaderboard('Final', leaderboard, idx, user)
        idx += 1


def process_leaderboards_11_12_LCQ(phase, competition, gender, athlete_event, user):
    i = 1
    leaderboards_final = []
    while i < 3:
        leaderboards = LeaderBoard.objects.filter(
            competition=competition,
            athlete_category_in_competition=athlete_event.category_in_competition, athlete_gender=gender,
            Q_Heat_number=i, round="LCQ"
        ).order_by('-Q_global_pontuation')
        leaderboards_final.extend(leaderboards[:1])
        i += 1
        idx = 1
        for leaderboard in leaderboards_final:
            set_new_leaderboard('Final', leaderboard, idx, user)
            idx += 1

    finalists = LeaderBoard.objects.filter(
        competition=competition,
        athlete_category_in_competition=athlete_event.category_in_competition, athlete_gender=gender,
        Q_Heat_number=1, round="Final"
    ).order_by('global_pontuation')

    idx = 1
    for leaderboard in finalists:
        leaderboard.round = 'Final'
        leaderboard.Q_Starting_list = idx
        leaderboard.Q_Heat_number = 1
        leaderboard.save()
        idx += 1


def process_leaderboards_11_12(phase, competition, gender, athlete_event, heat_system, user):
    i = 1
    leaderboards_lcq = []
    leaderboards_final = []
    while i < 3:
        leaderboards = LeaderBoard.objects.filter(
            competition=competition,
            athlete_category_in_competition=athlete_event.category_in_competition, athlete_gender=gender,
            Q_Heat_number=i
        ).order_by('-Q_global_pontuation')

        leaderboards_final.extend(leaderboards[:2])
        leaderboards = leaderboards[2:]
        leaderboards_lcq.extend(leaderboards)

        i += 1

    idx = 1
    leaderboards_final.sort(key=lambda x: getattr(x, 'global_pontuation'))
    for leaderboard in leaderboards_final:
        set_new_leaderboard('Final', leaderboard, idx, user)
        idx += 1

    riders_start_positions = [0, 0, 0, 0, 0, 0]
    riders_start_positions[0] = heat_system.Riders_LCQ_Heat1
    riders_start_positions[1] = heat_system.Riders_Q_Heat2
    active_heat = 2
    snake_control = 0
    valid_last = False
    leaderboards_lcq.sort(key=lambda x: getattr(x, 'global_pontuation'))
    for leaderboard in leaderboards_lcq:
        leader_board_new = LeaderBoard()
        leader_board_new.athlete = leaderboard.athlete
        leader_board_new.username = user
        leader_board_new.competition = competition
        leader_board_new.global_pontuation = leaderboard.global_pontuation
        leader_board_new.ranking = leaderboard.ranking
        leader_board_new.athlete_gender = leaderboard.athlete_gender
        leader_board_new.athlete_category_in_competition = leaderboard.athlete_category_in_competition
        leader_board_new.Q_1st_judge_atlhete_front_foot = leaderboard.Q_1st_judge_atlhete_front_foot
        leader_board_new.Q_1st_Judge_Last_name = leaderboard.Q_1st_Judge_Last_name
        leader_board_new.Q_1st_judge_first_name = leaderboard.Q_1st_judge_first_name
        leader_board_new.Q_1st_judge_iwwf_id = leaderboard.Q_1st_judge_iwwf_id
        leader_board_new.Q_2nd_judge_atlhete_front_foot = leaderboard.Q_2nd_judge_atlhete_front_foot
        leader_board_new.Q_2nd_Judge_Last_name = leaderboard.Q_2nd_Judge_Last_name
        leader_board_new.Q_2nd_judge_first_name = leaderboard.Q_2nd_judge_first_name
        leader_board_new.Q_2nd_judge_iwwf_id = leaderboard.Q_2nd_judge_iwwf_id
        leader_board_new.Q_3rd_judge_atlhete_front_foot = leaderboard.Q_3rd_judge_atlhete_front_foot
        leader_board_new.Q_3rd_Judge_Last_name = leaderboard.Q_3rd_Judge_Last_name
        leader_board_new.Q_3rd_judge_first_name = leaderboard.Q_3rd_judge_first_name
        leader_board_new.Q_3rd_judge_iwwf_id = leaderboard.Q_3rd_judge_iwwf_id
        leader_board_new.round = 'LCQ'
        if active_heat == 1:
            leader_board_new.Q_Heat_number = active_heat
            leader_board_new.Q_Heat_number = riders_start_positions[0]
            leader_board_new.save()
            riders_start_positions[0] -= 1
            if snake_control == 1:
                active_heat = int(heat_system.LCQ_Heats)
                snake_control = 0
            else:
                snake_control += 1
            continue

        if active_heat == 2:
            leader_board_new.Q_Heat_number = active_heat
            leader_board_new.Q_Starting_list = riders_start_positions[1]
            leader_board_new.save()
            riders_start_positions[1] -= 1
            if snake_control == 1:
                active_heat -= 1
                snake_control = 0
            else:
                snake_control += 1

            if not valid_last and int(heat_system.Q_Heats) == 2:
                valid_last = True
                active_heat -= 1
                snake_control = 0
            continue


def get_leaderboards(competition, category_in_competition, gender, global_pontuation, id, competition_round):
    leaderboard = LeaderBoard.objects.get(id=id)
    print("get_leaderboards")
    return LeaderBoard.objects.filter(
        competition=competition,
        athlete_category_in_competition=category_in_competition,
        athlete_gender=gender,
        Q_Heat_number=leaderboard.Q_Heat_number, round=competition_round
    ).order_by(global_pontuation)
