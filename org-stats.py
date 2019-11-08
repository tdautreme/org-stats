import argparse
from requests.exceptions import ConnectionError
from github import GithubException
from github import Github
from art import *
import random

class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

rcolors = [bcolors.PURPLE, bcolors.BLUE, bcolors.GREEN, bcolors.YELLOW, bcolors.CYAN, bcolors.RED]

class GithubUser:
    name = ""
    contribution = 0
    add_lines = 0
    remove_lines = 0
    productivity = 0
    precision = 0
    score = 0

def pc(contribution):
    return bcolors.BLUE + str(contribution) + bcolors.ENDC

def pal(add_lines):
    return bcolors.GREEN + str(add_lines) + "++" + bcolors.ENDC

def prl(remove_lines):
    return bcolors.RED + str(remove_lines) + "--" + bcolors.ENDC

def ppd(productivity):
    return bcolors.PURPLE + str(productivity) + "++-" + bcolors.ENDC

def ppc(precision):
    return bcolors.CYAN + str(precision) + "+--" + bcolors.ENDC

def pi(info):
    return bcolors.YELLOW + str(info) + bcolors.ENDC

def ps(score):
    return bcolors.BOLD + bcolors.UNDERLINE + bcolors.YELLOW + str(score) + bcolors.ENDC

def percent(number, total):
    return pi("{:.1f}".format(number / total * 100) + "%")

def perror(error):
    return bcolors.RED + "ERROR: " + str(error) + bcolors.ENDC

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--org', nargs=1, help="Github target organization name")
parser.add_argument('-u', '--username', nargs=1, help="Your github username (Optional)")
parser.add_argument('-p', '--password', nargs=1, help="Your github password (Optional)")
args = parser.parse_args()

ferror = False
if (args.username != None and args.password == None) or (args.username == None and args.password != None):
    print (perror("If you enter username, enter password too and vice-versa like python3 org-stats -u [username] -p [password]"))
    ferror = True

if args.org == None:
    print (perror("You must enter target org --org [target]"))
    ferror = True

if ferror:
    exit()

if args.username != None:
    g = Github(args.username[0], args.password[0])
else:
    g = Github()

try:
    target = g.get_organization(args.org[0])
except GithubException as e:
    print(perror(str(e.data['message'])))
    exit()
except ConnectionError as e:
    print(perror("Connexion failed"))
    exit()
except Exception as e:
    print(perror("Other: " + str(e)))
    exit()

print("")
print(random.choice(rcolors) + text2art("tdautreme","random") + bcolors.ENDC)
print("")

users = []

def user_exist(name):
    for user in users:
        if name == user.name:
            return True
    return False

def add_user(name, contribution, add_lines, remove_lines):
    productivity = add_lines + remove_lines
    precision = add_lines - remove_lines
    score = productivity + precision
    new_user = GithubUser()
    new_user.name = name
    new_user.contribution = contribution
    new_user.add_lines = add_lines
    new_user.remove_lines = remove_lines
    new_user.productivity = productivity
    new_user.precision = precision
    new_user.score = score
    users.append(new_user)
    return new_user

def update_user(name, contribution, add_lines, remove_lines):
    productivity = add_lines + remove_lines
    precision = add_lines - remove_lines
    score = productivity + precision
    for user in users:
        if user.name == name:
            user.contribution += contribution
            user.add_lines += add_lines
            user.remove_lines += remove_lines
            user.productivity += productivity
            user.precision += precision
            user.score += score
            return user

total_contribution = 0
total_add_lines = 0
total_remove_lines = 0

repos = target.get_repos()
if repos != None:
    for repo in repos:
        print (pi(repo.name))
        contributors = repo.get_stats_contributors()
        if contributors != None:
            for contributor in contributors:
                add_lines=0
                remove_lines=0
                weeks = contributor.weeks
                if weeks != None:
                    for week in weeks:
                        add_lines += week.a
                        remove_lines += week.d
                    total_contribution += contributor.total
                    total_add_lines += add_lines
                    total_remove_lines += remove_lines
                    if user_exist(contributor.author.login):
                        user = update_user(contributor.author.login, contributor.total, add_lines, remove_lines)
                    else:
                        user = add_user(contributor.author.login, contributor.total, add_lines, remove_lines)
                    print ("    " + user.name + " " + pc(user.contribution) + " " + pal(user.add_lines) + " " + prl(user.remove_lines) + " " + ppd(user.productivity) + " " + ppc(user.precision) + " " + ps(user.score))
        print("")


total_productivity = total_add_lines + total_remove_lines
total_precision = total_add_lines - total_remove_lines
total_score = total_productivity + total_precision

print(pi("____________________________________________________") + "\n")

print ("\n" + pi(">>> ") + pc("CONTRIBUTION") + pi(" RANK <<<"))
users.sort(key=lambda x: x.contribution, reverse=True)
rank = 1
for user in users:
    print ("    " + pi(rank) + " " + user.name + " " + pc(user.contribution) + " " + percent(user.contribution, total_contribution))
    rank += 1

print ("\n" + pi(">>> ") + pal("ADD LINES") + pi(" RANK <<<"))
users.sort(key=lambda x: x.add_lines, reverse=True)
rank = 1
for user in users:
    print ("    " + pi(rank) + " " + user.name + " " + pal(user.add_lines) + " " + percent(user.add_lines, total_add_lines))
    rank += 1

print ("\n" + pi(">>> ") + prl("REMOVE LINES") + pi(" RANK <<<"))
users.sort(key=lambda x: x.remove_lines, reverse=True)
rank = 1
for user in users:
    print ("    " + pi(rank) + " " + user.name + " " + prl(user.remove_lines) + " " + percent(user.remove_lines, total_remove_lines))
    rank += 1

print ("\n" + pi(">>> ") + ppd("PRODUCTIVITY (ADD + REMOVE)") + pi(" RANK <<<"))
users.sort(key=lambda x: x.productivity, reverse=True)
rank = 1
for user in users:
    print ("    " + pi(rank) + " " + user.name + " " + ppd(user.productivity) + " " + percent(user.productivity, total_productivity))
    rank += 1

print ("\n" + pi(">>> ") + ppc("PRECISION (ADD - REMOVE)") + pi(" RANK <<<"))
users.sort(key=lambda x: x.precision, reverse=True)
rank = 1
for user in users:
    print ("    " + pi(rank) + " " + user.name + " " + ppc(user.precision) + " " + percent(user.precision, total_precision))
    rank += 1

print ("\n" + pi(">>> TOTAL SCORE (PRODUCTIVITY + PRECISION) <<<"))
users.sort(key=lambda x: x.productivity + x.precision, reverse=True)
rank = 1
for user in users:
    print ("    " + pi(rank) + " " + user.name + " " + ps(user.score) + " " + percent(user.score, total_score) + "   [ " + pc(user.contribution) + " " + pal(user.add_lines) + " " + prl(user.remove_lines) + " " + ppd(user.productivity) + " " + ppc(user.precision) + " ]")
    rank += 1

print ("\nTarget " + pc(target.name) + " have " + pc(repos.totalCount) + " projects")
print (pc(total_contribution) + " " + pal(total_add_lines) + " " + prl(total_remove_lines) + " " + ppd(total_productivity) + " " + ppc(total_precision) + " " + ps(total_score))

print("")