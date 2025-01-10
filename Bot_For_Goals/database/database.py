from Bot_For_Goals.database.models import session,Goal,Task
from sqlalchemy.exc import SQLAlchemyError

def add_goal(title, deadline, user_id):
    try:
        new_goal = Goal(
            title=title,
            deadline=deadline,
            completed=False,
            user_id=user_id
        )
        session.add(new_goal)
        session.commit()
        return new_goal.id
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Ошибка базы данных: {e}")
        return None


def add_task(title, deadline, goal_id):
    try:
        goal = session.query(Goal).get(goal_id)
        if not goal:
            print(f"Цель с ID {goal_id} не найдена.")
            return None
        new_task = Task(
            title=title,
            deadline=deadline,
            goal_id=goal_id,
            completed=False
        )
        session.add(new_task)
        session.commit()
        print(f"Задача добавлена с ID: {new_task.id}")
        return new_task.id

    except Exception as e:
        session.rollback()
        print(f"Ошибка при добавлении задачи: {e}")
        return None


def get_goals():
    goals = session.query(Goal).all()
    return goals

def get_tasks(goal_id):
    return session.query(Task).filter_by(goal_id=goal_id).all()

def complete_goal(goal_id):
    try:
        goal = session.query(Goal).get(goal_id)

        if goal:
            if goal.completed:
                print(f"Цель с ID {goal_id} уже выполнена.")
                return "already_completed"
            goal.completed = True
            session.commit()
            return True
        else:
            print(f"Цель с ID {goal_id} не найдена.")
            return False
    except Exception as e:
        print(f"Ошибка при обновлении цели: {e}")
        return False

def complete_task(task_id):
    try:
        task = session.query(Task).get(task_id)
        if task:
            if task.completed:
                print(f"Задача с ID {task_id} уже выполнена.")
                return "already_completed"
            task.completed = True
            session.commit()
            return True
        else:
            print(f"Задача с ID {task_id} не найдена.")
            return False
    except Exception as e:
        print(f"Ошибка при обновлении задачи: {e}")
        return False

def delete_goal(goal_id):
    try:
        goal = session.query(Goal).get(goal_id)
        if goal:
            session.delete(goal)
            session.commit()
            return True
        else:
            print(f"Цель с ID {goal_id} не найдена.")
            return False
    except Exception as e:
        print(f"Ошибка при удалении цели: {e}")
        return False

def delete_task(task_id):
    try:
        task = session.query(Task).get(task_id)
        if task:
            session.delete(task)
            session.commit()
            return True
        else:
            print(f"Задача с ID {task_id} не найдена.")
            return False
    except Exception as e:
        print(f"Ошибка при удалении цели: {e}")
        return False

def get_statistics():
    try:
        goals = session.query(Goal).all()
        tasks = session.query(Task).all()
        total_goals = len(goals)
        completed_goals = sum(1 for goal in goals if goal.completed)
        incomplete_goals = total_goals - completed_goals
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task.completed)
        incomplete_tasks = total_tasks - completed_tasks
        goal_percent = (completed_goals / total_goals * 100) if total_goals > 0 else 0
        task_percent = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        stats = {
            "total_goals": total_goals,
            "completed_goals": completed_goals,
            "incomplete_goals": incomplete_goals,
            "goal_percent": goal_percent,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "incomplete_tasks": incomplete_tasks,
            "task_percent": task_percent
        }

        return stats
    except Exception as e:
        print(f"Ошибка при получении статистики: {e}")
        return None

def check_goal_exists(user_id):
    try:
        goal = session.query(Goal).filter_by(user_id=user_id).first()
        return goal is not None
    except SQLAlchemyError as e:
        print(f"Ошибка базы данных: {e}")
        return False